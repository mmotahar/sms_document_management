# -*- coding: utf-8 -*-
import logging
import json
from odoo import http, fields
from odoo.http import request
from odoo.addons.survey.controllers.main import Survey
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteSurveyExtend(Survey):
    # Printing routes
    @http.route(['/survey/print/<model("survey.survey"):survey>',
                 '/survey/print/<model("survey.survey"):survey>/<string:token>'
                 ],
                type='http', auth='public', website=True)
    def print_survey(self, survey, token=None, **post):
        '''Display an survey in printable view; if <token> is set, it will
        grab the answers of the user_input_id that has <token>.'''

        survey_question = request.env['survey.question']
        user_input = request.env['survey.user_input']
        user_input_line = request.env['survey.user_input_line']

        question_ids = survey_question.sudo().search(
            [('type', '=', 'upload_file'), ('survey_id', '=', survey.id)])
        user_input_id = user_input.sudo().search(
            [('token', '=', token), ('survey_id', '=', survey.id)])

        user_input_line_upload_file = []
        for question in question_ids:
            user_input_line = user_input_line.search([
                ('user_input_id', '=', user_input_id.id),
                ('survey_id', '=', survey.id),
                ('question_id', '=', question.id),
                ('answer_type', '=', 'upload_file')
            ])
            user_input_line_upload_file.append(user_input_line)
        return request.render(
            'survey.survey_print',
            {'survey': survey,
             'token': token,
             'page_nr': 0,
             'quizz_correction':
             True if survey.quizz_mode and token else False,
             'user_input_line_upload_file': user_input_line_upload_file})

    @http.route([
        '/survey/prefill/<model("survey.survey"):survey>/<string:token>',
        '/survey/prefill/<model("survey.survey"):survey>/<string:token>/'
        '<model("survey.page"):page>'],
                type='http', auth='public', website=True)
    def prefill(self, survey, token, page=None, **post):
        UserInputLine = request.env['survey.user_input_line']
        ret = {}

        # Fetch previous answers
        if page:
            previous_answers = UserInputLine.sudo().search([
                ('user_input_id.token', '=', token),
                ('page_id', '=', page.id)])
        else:
            previous_answers = UserInputLine.sudo().search(
                [('user_input_id.token', '=', token)])

        # Return non empty answers in a JSON compatible format
        for answer in previous_answers:
            if not answer.skipped:
                answer_tag = '%s_%s_%s' % (answer.survey_id.id,
                                           answer.page_id.id,
                                           answer.question_id.id)
                answer_value = None
                if answer.answer_type == 'free_text':
                    answer_value = answer.value_free_text
                elif answer.answer_type == 'text' and \
                        answer.question_id.type == 'textbox':
                    answer_value = answer.value_text
                elif answer.answer_type == 'text' and \
                        answer.question_id.type != 'textbox':
                    # here come comment answers for matrices,
                    # simple choice and multiple choice
                    answer_tag = "%s_%s" % (answer_tag, 'comment')
                    answer_value = answer.value_text
                elif answer.answer_type == 'number':
                    answer_value = str(answer.value_number)
                elif answer.answer_type == 'date':
                    answer_value = fields.Date.to_string(answer.value_date)
                elif answer.answer_type == 'suggestion' and \
                        not answer.value_suggested_row:
                    answer_value = answer.value_suggested.id
                elif answer.answer_type == 'suggestion' and \
                        answer.value_suggested_row:
                    answer_tag = "%s_%s" % (answer_tag,
                                            answer.value_suggested_row.id)
                    answer_value = answer.value_suggested.id
                elif answer.answer_type == 'upload_file' and answer.filename:
                    answer_value = answer.filename
                if answer_value:
                    ret.setdefault(answer_tag, []).append(answer_value)
                else:
                    _logger.warning(
                        "[survey] No answer has been found for "
                        "question %s marked as non skipped" % answer_tag)
        return json.dumps(ret, default=str)
