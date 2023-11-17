
from odoo import api, fields, models, _

import cairo

import base64

from io import BytesIO

from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)

from odoo.exceptions import UserError
from datetime import datetime, timedelta

import json
import pytz

class ProjectNativeReport(models.TransientModel):
    _name = "project.native.report"
    _description = "project.native.report"



    @api.model
    def _get_scale(self):
        value = [
            ('day_1hour', _('1-Hrs')),
            ('day_2hour', _('2-Hrs')),
            ('day_4hour', _('4-Hrs')),
            ('day_8hour', _('8-Hrs')),
            ('month_day', _('Day')),
            ('year_month', _('Month')),
            ('year_week', _('Week')),
            ('year_quarter', _('Quarter')),

        ]
        return value



    screen = fields.Boolean(string='Screen', default=False, readonly=True)

    project_id = fields.Many2one('project.project', 'Project', readonly=True)

    name = fields.Char(string='Name', default='Report', readonly=True)
    file_save = fields.Binary(string='Bin File', readonly=True)
    report_scale = fields.Selection('_get_scale',
                                       string='Scale',
                                       required=True,
                                       default='month_day')

    data_json = fields.Text(string='Data')
    pre_json = fields.Text(string='Precedessor')



    def rectangle_draw(self, ctx, width, start_w, start_h, size_w, size_h):

        ctx.set_line_width(width)

        ctx.rectangle(start_w, start_h, size_w, size_h)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke()



    def textwidth(self, ctx, text):
        x, y, width, height, dx, dy = ctx.text_extents(text)
        return width


    def huminize_duration(self, duration):

        text_list = ''
        if duration:

            attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
            human_readable = lambda delta: ['%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
                                            for attr in attrs if getattr(delta, attr)]

            text_list = human_readable(relativedelta(seconds=duration))

        return ' '.join(text_list)

    def draw_info(self, ctx, plot_param, from_left):

        tz_name = self.env.context.get('tz') or self.env.user.tz

        from_top = plot_param["margin_top"]
        line_width = plot_param["line_width"]
        font = plot_param["font_face"]

        ctx.select_font_face(font)

        idx_col = "tzname: {}".format(tz_name)

        space_lft = 2

        pad_from_left = from_left + space_lft + (2 * line_width)
        pad_from_top = from_top - 12

        ctx.move_to(pad_from_left, pad_from_top)
        ctx.show_text(idx_col)




    def col_draw_wbs(self, ctx, data_list, plot_param, from_left):


        from_top = plot_param["margin_top"]
        line_width = plot_param["line_width"]
        font = plot_param["font_face"]

        ctx.select_font_face(font)

        pad_from_left = 0
        idx_col_len = []
        space_lft = 2
        space_rgh = 5

        i_next = 1

        for idx, val in enumerate(data_list):

            if val["wbs"]:
                idx_col = val["wbs"]
                i_next = 0
            else:
                if val["separate"]:
                    i_next = 0
                    idx_col = ""
                else:
                    idx_col = i_next

            idx_col = "{}".format(idx_col)

            pad_from_left = from_left + space_lft + (2 * line_width)
            pad_from_top = from_top + 12 + line_width + (idx * 20)

            ctx.move_to(pad_from_left, pad_from_top)
            ctx.show_text(idx_col)

            idx_col_width = self.textwidth(ctx, idx_col)
            idx_col_len.append(idx_col_width + space_rgh)

            i_next += 1


        if idx_col_len:
            from_left = int(max(idx_col_len)) + pad_from_left
            ctx.set_source_rgba(0, 0, 0, 0.5)
            #vertical Line
            ctx.set_dash([])
            ctx.set_line_width(0.5)
            ctx.set_line_width(line_width)
            ctx.move_to(from_left, from_top)
            ctx.line_to(from_left, plot_param["margin_top"]+plot_param["plot_height"])
            ctx.stroke()

        return from_left



    def col_draw_stuff(self, ctx, data_list, plot_param, from_left):

        from_top = plot_param["margin_top"]
        line_width = plot_param["line_width"]
        font = plot_param["font_face"]

        ctx.select_font_face(font)

        pad_from_left = 0
        idx_col_len = []

        space_lft = 2
        space_rgh = 5

        for idx, val in enumerate(data_list):

            if val["stuff"]:
                idx_col = val["stuff"]

                idx_col = "{}".format(idx_col)

                pad_from_left = from_left + space_lft + (2 * line_width)
                pad_from_top = from_top + 12 + line_width + (idx * 20)

                ctx.move_to(pad_from_left, pad_from_top)
                ctx.show_text(idx_col)

                idx_col_width = self.textwidth(ctx, idx_col)
                idx_col_len.append(idx_col_width + space_rgh)


        if idx_col_len:
            from_left = int(max(idx_col_len)) + pad_from_left
            ctx.set_source_rgba(0, 0, 0, 0.5)
            # vertical Line
            ctx.set_dash([])
            ctx.set_line_width(0.5)
            ctx.set_line_width(line_width)
            ctx.move_to(from_left, from_top)
            ctx.line_to(from_left, plot_param["margin_top"] + plot_param["plot_height"])
            ctx.stroke()

        return from_left

    def col_draw_item(self, ctx, data_list, plot_param, from_left):

        from_top = plot_param["margin_top"]
        line_width = plot_param["line_width"]
        font = plot_param["font_face"]
        ctx.set_font_size(10)

        ctx.select_font_face(font)

        pad_from_left = 0
        idx_col_len = []

        padding_depth = 15
        space_lft = 2
        space_rgh = 5

        for idx, val in enumerate(data_list):

            if val["name"]:
                idx_col = val["name"]

                idx_col = "{}".format(idx_col)

                if val["subtask_count"] > 0:
                    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                else:
                    ctx.select_font_face(font)

                level = val["sorting_level"]
                paddepth = padding_depth * level

                pad_from_left = from_left + space_lft + (2 * line_width) + paddepth
                pad_from_top = from_top + 12 + line_width + (idx * 20)

                ctx.move_to(pad_from_left, pad_from_top)
                ctx.show_text(idx_col)

                idx_col_width = self.textwidth(ctx, idx_col)
                idx_col_len.append(idx_col_width + space_rgh)


        if idx_col_len:
            from_left = int(max(idx_col_len)) + pad_from_left
            ctx.set_source_rgba(0, 0, 0, 0.5)
            # vertical Line
            ctx.set_dash([])
            ctx.set_line_width(0.5)
            ctx.set_line_width(line_width)
            ctx.move_to(from_left, from_top)
            ctx.line_to(from_left, plot_param["margin_top"] + plot_param["plot_height"])
            ctx.stroke()

        return from_left


    def col_draw_custom(self, ctx, data_list, plot_param, from_left):

        from_top = plot_param["margin_top"]
        line_width = plot_param["line_width"]
        font = plot_param["font_face"]

        ctx.select_font_face(font)
        space_lft = 2
        space_rgh = 5
        ctx.set_font_size(9)

        for custom_field in plot_param["custom_fields"]:

            pad_from_left = 0
            idx_col_len = []

            for idx, val in enumerate(data_list):

                if val[custom_field]:
                    idx_col = val[custom_field]

                    if isinstance(idx_col, datetime):
                        idx_col = fields.Datetime.to_string(idx_col)
                    else:
                        idx_col = "{}".format(idx_col)

                    pad_from_left = from_left + space_lft + (2 * line_width)
                    pad_from_top = from_top + 12 + line_width + (idx * 20)

                    ctx.move_to(pad_from_left, pad_from_top)
                    ctx.show_text(idx_col)

                    idx_col_width = self.textwidth(ctx, idx_col)
                    idx_col_len.append(idx_col_width + space_rgh)


            if idx_col_len:
                from_left = int(max(idx_col_len)) + pad_from_left
                ctx.set_source_rgba(0, 0, 0, 0.5)
                # vertical Line
                ctx.set_dash([])
                ctx.set_line_width(0.5)
                ctx.set_line_width(line_width)
                ctx.move_to(from_left, from_top)
                ctx.line_to(from_left, plot_param["margin_top"] + plot_param["plot_height"])
                ctx.stroke()

        return from_left


    def col_draw_duration(self, ctx, data_list, plot_param, from_left):

        from_top = plot_param["margin_top"]
        line_width = plot_param["line_width"]
        font = plot_param["font_face"]
        ctx.set_font_size(10)

        ctx.select_font_face(font)

        text_duration_list = []
        len_duration = []

        for idx, val in enumerate(data_list):

            if val["subtask_count"] > 0:
                ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            else:
                ctx.select_font_face(font)

            text_duration = self.huminize_duration(val["duration"])
            text_duration_width = self.textwidth(ctx, text_duration)
            text_duration_list.append([text_duration, text_duration_width, val["subtask_count"] ])

            len_duration.append(text_duration_width)

        from_left = max(len_duration) + from_left + 5


        # draw duration
        ctx.select_font_face(font)
        for idx, val in enumerate(text_duration_list):

            if val[2] > 0:
                ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            else:
                ctx.select_font_face(font)

            ctx.move_to(from_left - val[1], from_top + 12 + line_width + (idx * 20))
            ctx.show_text(val[0])

        return from_left



    def item_draw(self, ctx, data_list,  plot_param, calc_width=False):

        from_left = plot_param["margin_left"]
        from_top = plot_param["margin_top"]
        line_width = plot_param["line_width"]
        font = plot_param["font_face"]

        ctx.set_line_width(line_width)

        self.draw_info(ctx, plot_param, from_left)
        # WBS Column
        from_left = self.col_draw_wbs(ctx, data_list, plot_param, from_left)

        # Stuff Column
        from_left = self.col_draw_stuff(ctx, data_list, plot_param, from_left)

        # item Name Column
        from_left = self.col_draw_item(ctx, data_list, plot_param, from_left)

        # Custom Column
        from_left = self.col_draw_custom(ctx, data_list, plot_param, from_left)

        # Custom Column
        from_left = self.col_draw_duration(ctx, data_list, plot_param, from_left)


        duration_from = from_left + 5
        if calc_width:
            return duration_from

        ctx.stroke()

        #vertical line finish items

        ctx.set_dash([])
        ctx.set_line_width(0.5)
        ctx.set_line_width(plot_param["line_width"])
        ctx.move_to(plot_param["item_width"], plot_param["margin_top"])
        ctx.line_to(plot_param["item_width"], plot_param["margin_top"]+plot_param["plot_height"])
        ctx.stroke()



        # #dash line horizontal items
        ctx.set_source_rgb(0.5, 0.5, 0.5)
        ctx.set_line_width(0.5)
        for i in range(1, plot_param["tasks_list_len"]):
            ctx.set_dash([2.0])

            draw_line_top = plot_param["margin_top"] + (i*plot_param["element_height"])
            ctx.move_to(plot_param["margin_left"], draw_line_top)
            ctx.line_to(plot_param["item_width"], draw_line_top)
            ctx.stroke()

        ctx.set_dash([])






    def first_date_of_month(self, dt):

        first_day = dt.replace(day=1)
        dt_day = dt.day

        if 4 < dt_day:
            first = dt - timedelta(days=4)
        else:
            first = first_day

        return first.replace(minute=0, hour=0, second=0)



    def last_date_of_month(self, dt):

        next_month = dt.replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)

        dt_day = dt.day

        if dt_day > 15:
            first = dt + timedelta(days=12)
        else:
            first = last_day

        return first.replace(minute=0, hour=0, second=0)




    def min_max_range(self, task_ids):

        f_date_start = "date_start"
        f_date_end = "date_end"
        date_start = None
        date_end = None

        date_start_range = []
        date_end_range = []

        for item in task_ids:

            # r_date_start = fields.Datetime.from_string(item[f_date_start])
            # r_date_end = fields.Datetime.from_string(item[f_date_end])

            r_date_start = item[f_date_start]
            r_date_end = item[f_date_end]

            if not r_date_start:
                r_date_start = r_date_end
            if not r_date_end:
                r_date_end = r_date_start

            if r_date_start and r_date_end:
                date_start_range.append(r_date_start)
                date_end_range.append(r_date_end)

        if date_start_range:
            date_start_range = min(date_start_range)
            date_start = self.first_date_of_month(date_start_range)




        if date_end_range:
            date_end_range = max(date_end_range)
            date_end = self.last_date_of_month(date_end_range)

        return date_start, date_end



    def get_scale(self, date_start, date_end, plot_param):

        first_day_scale = date_start.timestamp()
        time_scale = date_end.timestamp() - date_start.timestamp()

        timeline_width = 0
        px_scale = 0

        if plot_param["scale"] == "year_week":

            for dt in self.daterange(date_start, date_end, type_range="week"):
                timeline_width += 1

        elif plot_param["scale"] == "year_month":

            for dt in self.daterange(date_start, date_end, type_range="month"):
                timeline_width += 1

        elif plot_param["scale"] == "month_day":

            for dt in self.daterange(date_start, date_end, type_range="day"):
                timeline_width += 1

        elif plot_param["scale"] == "day_8hour":

            for dt in self.daterange(date_start, date_end, type_range="8hour"):
                timeline_width += 1

        elif plot_param["scale"] == "day_4hour":

            for dt in self.daterange(date_start, date_end, type_range="4hour"):
                timeline_width += 1

        elif plot_param["scale"] == "day_2hour":

            for dt in self.daterange(date_start, date_end, type_range="2hour"):
                timeline_width += 1

        elif plot_param["scale"] == "day_1hour":

            for dt in self.daterange(date_start, date_end, type_range="1hour"):
                timeline_width += 1

        elif plot_param["scale"] == "year_quarter":

            for dt in self.daterange(date_start, date_end, type_range="quarter"):
                timeline_width += 1



        if timeline_width:
            timeline_width = plot_param["cell_scale"] * timeline_width
            px_scale = time_scale / timeline_width

        return first_day_scale, px_scale, timeline_width


    def daterange(self, date1, date2, type_range):


        result = []
        if type_range == "year":
            while date1 <= date2:
                result.append(date1)
                date1 += relativedelta(years=1)
            result.append(date2)


        elif type_range == "quarter":
            while date1 <= date2:
                result.append(date1)
                date1 += relativedelta(weeks=3)

        elif type_range == "week":
            while date1 <= date2:
                result.append(date1)
                date1 += relativedelta(weeks=1)

        elif type_range == "day":
            while date1 <= date2:
                result.append(date1)
                date1 += relativedelta(days=1)

        elif type_range == "month":

            date2_last_day = self.last_day_of_month(date2)

            while date1 <= date2_last_day:
                result.append(date1)
                date1 += relativedelta(months=1)

        elif type_range == "8hour":
            while date1 <= date2:
                result.append(date1)
                date1 += relativedelta(hours=8)

        elif type_range == "4hour":
            while date1 <= date2:
                result.append(date1)
                date1 += relativedelta(hours=4)

        elif type_range == "2hour":
            while date1 <= date2:
                result.append(date1)
                date1 += relativedelta(hours=2)

        elif type_range == "1hour":
            while date1 <= date2:
                result.append(date1)
                date1 += relativedelta(hours=1)



        return result



    def item_size(self, tasks_list, plot_param, ctx=None):

        dummy_width = 500

        plot_width = dummy_width + plot_param["margin_left"]

        # start draw
        if not ctx:
            buffered = BytesIO()
            report_surface = cairo.PDFSurface(buffered, plot_param["timeline_width"],  plot_param["plot_height"])
            ctx = cairo.Context(report_surface)
            # svg = cairo.SVGSurface(buffered, dummy_width + plot_param["timeline_width"],  plot_param["plot_height"])
            # ctx = cairo.Context(svg)

        # border
        self.rectangle_draw(ctx, plot_param["line_width"],
                                 plot_param["margin_left"],
                                 plot_param["margin_top"],
                                 plot_width,
                                 plot_param["plot_height"])

        item_width = self.item_draw(ctx, tasks_list, plot_param , calc_width=True)


        return item_width



    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)

    def convert_datetime(self, dt_date):

        tz_name = self.env.context.get('tz') or self.env.user.tz

        if not isinstance(dt_date, datetime):

            try:
                dt_date = fields.Datetime.from_string(dt_date)
            finally:
                pass

        if isinstance(dt_date, datetime):

            if tz_name:
                user_tz = pytz.timezone(tz_name)
                dt_date = dt_date.replace(tzinfo=pytz.utc).astimezone(user_tz)

        return dt_date


    def record_params(self, val):

        params = {
            "id": val.id,
            "name": val.name,
            "duration": val.native_duration,
            "date_start": self.convert_datetime(val.date_start),
            "date_end": self.convert_datetime(val.date_end),
            "sorting_level": val.sorting_level,
            "subtask_count": val.subtask_count,
            "wbs": None,
            "stuff": "",
            "separate": False,
            "color_gantt": val.color_gantt,

        }

        return params

    def get_resource(self, tasks, screen=False):
        resource_list = []
        if screen and self.pre_json:
            pass
        else:
            uids = map(lambda x: x["id"], tasks)
            task_ids = list(uids)
            domain = [('task_id', 'in', task_ids)]

            resource = self.env['project.task.resource.link'].sudo().search(domain)


            for val in resource:
                pre_params = {
                    "task_id": val.task_id.id,
                    "res_name": val.resource_id.name
                }
                resource_list.append(pre_params)
        return resource_list

    def get_predecessor(self, tasks, screen=False):
        predecessors_list = []
        if screen and self.pre_json:
            pre_data = json.loads(self.pre_json)
            pre_params = {
                "task_id": 0,
                "parent_task_id": 0,
                "type": None
            }

            for val in pre_data:

                for k, v in pre_params.items():
                    if k not in val:
                        val[k] = v

            return pre_data


        else:
            uids = map(lambda x: x["id"], tasks)
            task_ids = list(uids)
            domain = [('task_id', 'in', task_ids)]

            predecessors = self.env['project.task.predecessor'].sudo().search(domain)


            for val in predecessors:
                pre_params = {
                    "task_id": val.task_id.id,
                    "parent_task_id": val.parent_task_id.id,
                    "type": val.type
                }
                predecessors_list.append(pre_params)
        return predecessors_list

    def get_source(self, screen=False):

        prj_params = {
            "id": 0,
            "name": "name",
            "duration": None,
            "date_start": None,
            "date_end": None,
            "sorting_level": 0,
            "subtask_count": 1,
            "wbs": None,
            "stuff": "",
            "separate": True,
            "color_gantt": None
        }


        if screen:

            data_json = json.loads(self.data_json)

            for val in data_json:

                for k, v in prj_params.items():
                    if k not in val:
                        val[k] = v


                val["date_start"] = self.convert_datetime(val["date_start"])
                val["date_end"] = self.convert_datetime(val["date_end"])

            return data_json


        else:
            # Task List
            project_id = self.project_id.id

            domain = [('project_id', '=', project_id), '|', ('active', '=', True), ('active', '=', False)]

            self.env['project.task'].do_sorting(project_id)
            arch_tasks = self.env['project.task'].sudo().search(domain)
            tasks_data = arch_tasks.sorted(key=lambda x: x.sorting_seq)
            tasks_list_len = len(tasks_data)
            tasks_list = []

            prj_params = {
                "id": project_id * -1,# Negative value for project
                "name": self.project_id.name,
                "duration": None,
                "date_start": None,
                "date_end": None,
                "sorting_level": 0,
                "subtask_count": 1,
                "wbs": None,
                "stuff": "",
                "separate": True,
                "color_gantt": None
            }

            tasks_list.append(prj_params)

            for val in tasks_data:

                params = self.record_params(val)

                if val.plan_action:
                    params["stuff"] = "!"

                tasks_list.append(params)

            return tasks_list


    def header_draw(self, ctx, plot_param):

        first_header = "month"
        second_header = "day"
        first_header_count = 0


        if plot_param["scale"] == "year_week":
            first_header = "year"
            second_header = "week"

        elif plot_param["scale"] == "year_month":
            first_header = "year"
            second_header = "month"


        elif plot_param["scale"] == "month_day":
            first_header = "month"
            second_header = "day"


        elif plot_param["scale"] == "day_8hour":
            first_header = "day"
            second_header = "8hour"


        elif plot_param["scale"] == "day_4hour":
            first_header = "day"
            second_header = "4hour"


        elif plot_param["scale"] == "day_2hour":
            first_header = "day"
            second_header = "2hour"

        elif plot_param["scale"] == "day_1hour":
            first_header = "day"
            second_header = "1hour"


        next_cell = plot_param["item_width"]

        f_header = False
        plot_first_header = True

        for dt in self.daterange(plot_param["date_start"], plot_param["date_end"], second_header):


            ctx.set_source_rgba(0, 0, 0, 0.5)
            f_header_compare = False

            if first_header == "day":
                f_header_compare = "{}".format(dt.strftime("%a %b %d - %Y"))

            elif first_header == "year":
                f_header_compare = "{}".format(dt.strftime("%Y"))

            elif first_header == "month":
                f_header_compare = "{}".format(dt.strftime("%b - %Y"))


            if f_header_compare and f_header != f_header_compare:
                f_header = f_header_compare
                plot_first_header = True

            if plot_first_header:
                ctx.move_to(next_cell, plot_param["margin_top"] - 28)
                ctx.line_to(next_cell, plot_param["margin_top"] + plot_param["plot_height"])

                ctx.move_to(next_cell + 4, plot_param["margin_top"] - 18)
                ctx.set_font_size(10)
                ctx.show_text(f_header)

                plot_first_header = False


            ctx.set_source_rgba(0, 0, 0, 0.5)
            ctx.set_font_size(10)

            draw_text = ""

            if second_header == "week":
                draw_text = "{}".format(dt.strftime("%W"))

            elif second_header == "month":
                draw_text = "{}".format(dt.strftime("%b"))

            elif second_header == "day":
                draw_text = "{}".format(dt.strftime("%d"))

            elif second_header == "8hour":
                draw_text = "{}".format(dt.strftime("%H:%M"))
            elif second_header == "4hour":
                draw_text = "{}".format(dt.strftime("%H:%M"))
            elif second_header == "2hour":
                draw_text = "{}".format(dt.strftime("%H:%M"))
            elif second_header == "1hour":
                draw_text = "{}".format(dt.strftime("%H:%M"))

            ctx.move_to(next_cell + 4, plot_param["margin_top"] - 4)
            ctx.show_text(draw_text)
            ctx.move_to(next_cell, plot_param["margin_top"] - 14)

            ctx.line_to(next_cell, plot_param["margin_top"] + plot_param["plot_height"])

            ctx.stroke()

            if dt.isoweekday() in [6, 7]:
                ctx.set_source_rgba(0, 0, 0, 0.05)
                ctx.rectangle(next_cell, plot_param["margin_top"] - 14, plot_param["cell_scale"], plot_param["plot_height"] + 14)
                ctx.fill()
                ctx.stroke()


            next_cell = next_cell + plot_param["cell_scale"]
            # ctx.move_to(next_cell + 4, plot_param["margin_top"] - 4)



        ctx.set_source_rgba(0, 0, 0, 0.5)
        ctx.stroke()

        next_cell = plot_param["item_width"]

        # Header horizontal line
        ctx.set_line_width(0.5)
        ctx.move_to(next_cell, plot_param["margin_top"] - 14)
        ctx.line_to(next_cell + plot_param["timeline_width"], plot_param["margin_top"] - 14)

        ctx.move_to(next_cell, plot_param["margin_top"] - 28)
        ctx.line_to(next_cell + plot_param["timeline_width"], plot_param["margin_top"] - 28)
        ctx.stroke()

        #####
        next_cell = plot_param["item_width"]
        ctx.move_to(next_cell, plot_param["margin_top"] - 28)
        ctx.line_to(next_cell, plot_param["margin_top"])
        ctx.move_to(next_cell + 4, plot_param["margin_top"] - 18)

    def bar_draw(self, ctx, tasks_list, plot_param, resource_list):

        step_left = plot_param["item_width"]
        step_top = plot_param["margin_top"]
        ctx.set_line_width(0.5)
        bar_height = 12

        for numbar, task_bar in enumerate(tasks_list):

            if task_bar["date_start"] and task_bar["date_end"]:

                task_start_time = task_bar["date_start"].timestamp()
                task_stop_time = task_bar["date_end"].timestamp()

                if task_stop_time >= task_start_time:

                    task_start_pxscale = round( (task_start_time - plot_param["first_day_scale"]) / plot_param["px_scale"])
                    task_stop_pxscale = round( (task_stop_time - plot_param["first_day_scale"]) / plot_param["px_scale"])

                    if task_start_pxscale == task_stop_pxscale:
                        task_stop_pxscale = task_stop_pxscale+1

                    bar_left = task_start_pxscale + plot_param["item_width"]
                    bar_width = task_stop_pxscale - task_start_pxscale

                    color_bar_gen = [210/100, 105/100, 30/100, 0.5] #210,105,30  112,128,144
                    if task_bar["color_gantt"]:
                        rgba = task_bar["color_gantt"].replace("rgba(", "")
                        rgba = rgba.replace(")", "")
                        rgba = rgba.split(",")
                        color_bar_gen = [float(rgba[0])/100, float(rgba[1])/100, float(rgba[2])/100, 0.5]

                    if task_bar["subtask_count"]:
                        color_bar_gen = [0.5, 0.5, 0.5, 0.25]

                    ctx.set_source_rgba(*color_bar_gen)

                    x = bar_left
                    y = plot_param["margin_top"] + (numbar*plot_param["element_height"])
                    width = bar_width
                    height = bar_height

                    element = {
                        'task_id': task_bar["id"],
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height}


                    # bar
                    ctx.rectangle(x, y, width, height)
                    ctx.fill()

                    # bar border
                    ctx.rectangle(x, y, width, height)
                    ctx.set_source_rgba(0.5, 0.5, 0.5, 0.35)
                    ctx.set_line_width(1)
                    ctx.stroke()

                    task_bar["bar_elemnt"] = element
                    task_bar["bar_left"] = bar_left
                    task_bar["bar_width"] = bar_width


                    ctx.set_source_rgba(0.5, 0.5, 0.5, 0.80)
                    ctx.move_to(bar_left, plot_param["margin_top"] + (numbar*plot_param["element_height"]) + bar_height-3)
                    ctx.set_font_size(9)


                    bar_text = "{}".format(task_bar["name"])

                    resource_toprint = list(filter(lambda x: x["task_id"] == task_bar["id"], resource_list))
                    if resource_toprint:
                        res_text = ', '.join(str(x["res_name"]) for x in resource_toprint)
                        bar_text = "{} - res: {}".format(bar_text, res_text)

                    # bar_text_width = self.textwidth(ctx, bar_text)

                    # if bar_text_width > bar_width:
                    #
                    #     bar_teext_len = len(bar_text)
                    #     gg= ((bar_width - 10) * bar_teext_len) / bar_text_width
                    #     bar_text = bar_text[:int(round(gg))]

                    ctx.show_text(bar_text)
                    ctx.set_source_rgba(0.2, 0.15, 0.07, 1)


        ctx.stroke()

    def arrow_step(self, bar_from, bar_to, arrow_type):

        step = [None, None]
        from_x = bar_from["x"]
        to_x = bar_to["x"]

        if arrow_type == "FF":
            from_x = bar_from["x"] + bar_from["width"]
            to_x = bar_to["x"] + bar_to["width"]

        if arrow_type == "SF":
            to_x = bar_to["x"] + bar_to["width"]

        if arrow_type == "FS":
            from_x = bar_from["x"] + bar_from["width"]

        if bar_to["y"] < bar_from["y"]:
            #go up
            if to_x - from_x > 15:
                #go right
                if arrow_type == "SS":
                    step = ["up_", "right>"]
                if arrow_type == "SF":
                    step = ["up", "right", "up_", "left<"]
                if arrow_type == "FS":
                    step = ["up_", "right>"]
            else:
                #go left
                if arrow_type == "SS":
                    step = ["up", "left", "up_", "right>"]
                if arrow_type == "SF":
                    step = ["up_", "left<"]
                if arrow_type == "FS":
                    step = ["up", "left", "up_", "right>"]

            if arrow_type == "FF":
                step = ["up_", "left<"]
                if to_x > from_x:
                    step = ["up", "right", "up_", "left<"]


        if bar_to["y"] > bar_from["y"]:
            #go down
                if to_x - from_x > 15:
                    #go right
                    if arrow_type == "SS":
                        step = ["down_", "right>"]

                    if arrow_type == "SF":
                        step = ["down", "right", "down_", "left<"]

                    if arrow_type == "FS":
                        step = ["down_", "right>"]
                    if arrow_type == "FF":
                        step = ["down", "right", "down_", "left<"]

                else:
                    #go left
                    if arrow_type == "SS":
                        step = ["down", "left", "down_", "right>"]

                    if arrow_type == "SF":
                        step = ["down_", "left<"]

                    if arrow_type == "FS":
                        step = ["down", "left","down_", "right>"]

                    if arrow_type == "FF":
                        step = ["down_", "left<"]
                        if to_x >= from_x:
                            step = ["down", "right", "down_", "left<"]

        return step


    def arrow_draw(self, ctx, tasks_list, predecessor_list, plot_param):

        for predecessor in predecessor_list:
            to_task = predecessor["task_id"]
            from_task = predecessor["parent_task_id"]

            from_obj_list = list(filter(lambda x: x["id"] == from_task, tasks_list))
            to_obj_list = list(filter(lambda x: x["id"] == to_task, tasks_list))

            type_direction = predecessor["type"]

            ctx.set_dash([])
            ctx.set_line_width(0.8)

            if from_obj_list and to_obj_list:

                from_obj = from_obj_list[0]
                to_obj = to_obj_list[0]


                from_x = from_obj["bar_elemnt"]["x"]
                from_width = from_obj["bar_elemnt"]["width"]
                from_y = from_obj["bar_elemnt"]["y"]

                to_x = to_obj["bar_elemnt"]["x"]
                to_width = to_obj["bar_elemnt"]["width"]
                to_y = to_obj["bar_elemnt"]["y"]+6

                #start and end point

                if type_direction == "FF":
                    from_x = from_x + from_width + 5
                    to_x = to_x + to_width + 10

                if type_direction == "SF":
                    from_x = from_x - 5
                    to_x = to_x + to_width + 10

                if type_direction == "FS":
                    from_x = from_x + from_width + 5
                    to_x = to_x - 10

                if type_direction == "SS":
                    to_x = to_x - 10
                    from_x = from_x - 5

                # start from middle bar
                step_x = from_x
                step_y = from_y + 6
                ctx.move_to(step_x, step_y)

                ctx.arc(step_x, step_y, 1, 0, 2 * 3.14)

                ctx.move_to(step_x, step_y)

                steps = self.arrow_step(from_obj["bar_elemnt"], to_obj["bar_elemnt"], predecessor["type"] )
                for step in steps:
                    if step == "up":
                        step_y = step_y-10
                        ctx.line_to(step_x, step_y)

                    if step == "up_":
                        ctx.line_to(step_x, to_y)

                    if step == "left":
                        step_x = to_x-10
                        ctx.line_to(step_x, step_y)

                    if step == "right":
                        step_x = to_x+10
                        ctx.line_to(step_x, step_y)

                    if step == "right>":
                        ctx.line_to(to_x, to_y)
                        self.arrow_right(ctx, to_x, to_y-1.5, 3, 3, 2, 2)

                    if step == "left<":
                        ctx.line_to(to_x, to_y)
                        self.arrow_left(ctx, to_x, to_y-1.5, 3, 3, 2, 2)

                    if step == "down":
                        step_y = step_y+10
                        ctx.line_to(step_x, step_y)

                    if step == "down_":
                        ctx.line_to(step_x, to_y)

            ctx.stroke()

    def arrow_right(self, ctx, x, y, width, height, a, b):
        ctx.move_to(x, y + b)
        ctx.line_to(x, y + height - b)
        ctx.line_to(x + a, y + height - b)
        ctx.line_to(x + a, y + height)
        ctx.line_to(x + width, y + height/2)
        ctx.line_to(x + a, y)
        ctx.line_to(x + a, y + b)
        ctx.close_path()

    def arrow_left(self, ctx, x, y, width, height, a, b):
        ctx.move_to(x, y + b)
        ctx.line_to(x, y + height - b)
        ctx.line_to(x - a, y + height - b)
        ctx.line_to(x - a, y + height)
        ctx.line_to(x - width, y + height/2)
        ctx.line_to(x - a, y)
        ctx.line_to(x - a, y + b)
        ctx.close_path()


    # @api.multi
    def action_report(self):

        allow = self.env['res.users'].has_group('project_native_report_advance.group_project_native_pdf_export')

        if allow:
            # SOURCE

            tasks_list = self.get_source(self.screen)
            predecessor_list = self.get_predecessor(tasks_list, self.screen)
            resource_list = self.get_resource(tasks_list, self.screen)

            tasks_list_len = len(tasks_list)
            custom_fields = ["date_start", "date_end"]

            scale = "month_day"
            cell_scale = 20

            if self.report_scale == "day_1hour":
                scale = "day_1hour"
                cell_scale = 40

            elif self.report_scale == "day_2hour":
                scale = "day_2hour"
                cell_scale = 40

            elif self.report_scale == "day_4hour":
                scale = "day_4hour"
                cell_scale = 40

            elif self.report_scale == "day_8hour":
                scale = "day_8hour"
                cell_scale = 40

            elif self.report_scale == "year_month":
                scale = "year_month"
                cell_scale = 40

            elif self.report_scale == "year_week":
                scale = "year_week"
                cell_scale = 40

            elif self.report_scale == "year_month":
                scale = "year_month"
                cell_scale = 40

            elif self.report_scale == "year_quarter":
                scale = "year_quarter"
                cell_scale = 40

            plot_param = {
                "font_face": "Liberation Sans",
                "margin_left": 20,
                "margin_right": 20,
                "margin_buttom": 20,
                "margin_top": 10,
                "element_height": 20,
                "cell_scale": cell_scale,
                "line_width": 1,
                "head_height": 50,
                "tasks_list_len": tasks_list_len,
                "scale": scale,
                "custom_fields": custom_fields

            }

            plot_param["margin_top"] = plot_param["head_height"] + plot_param["margin_top"]

            # min max date
            date_start, date_end = self.min_max_range(tasks_list)

            if date_start and date_end:

                plot_param["date_start"] = date_start
                plot_param["date_end"] = date_end

                # scale for time
                first_day_scale, px_scale, timeline_width, = self.get_scale(date_start, date_end, plot_param)
                plot_param["first_day_scale"] = first_day_scale
                plot_param["px_scale"] = px_scale
                plot_param["timeline_width"] = timeline_width

                # total height
                plot_param["plot_height"] = tasks_list_len * plot_param["element_height"]
                plot_param["surface_height"] = plot_param["plot_height"] + plot_param["margin_top"] + plot_param[
                    "margin_buttom"]

                plot_param["date_start"] = date_start
                plot_param["date_end"] = date_end
                plot_param["first_day_scale"] = first_day_scale
                plot_param["px_scale"] = px_scale
                plot_param["timeline_width"] = timeline_width

                # items width with fake CTX
                plot_param["item_width"] = self.item_size(tasks_list, plot_param)

                # Real Size
                plot_param["plot_width"] = plot_param["item_width"] + plot_param["timeline_width"]
                plot_param["surface_width"] = plot_param["margin_left"] + plot_param["plot_width"] + plot_param[
                    "margin_right"]

                # Generate CTX
                buffered = BytesIO()

                report_surface = cairo.PDFSurface(buffered, plot_param["surface_width"], plot_param["surface_height"])
                ctx = cairo.Context(report_surface)

                # svg = cairo.SVGSurface(buffered, plot_param["surface_width"], plot_param["surface_height"])
                # ctx = cairo.Context(svg)

                self.rectangle_draw(ctx, plot_param["line_width"],
                                    plot_param["margin_left"],
                                    plot_param["margin_top"],
                                    plot_param["plot_width"],
                                    plot_param["plot_height"])

                ctx.stroke()

                # ITEMS DRAW
                self.item_draw(ctx, tasks_list, plot_param)

                # HEADER DRAW
                self.header_draw(ctx, plot_param)

                # BAR DRAW
                self.bar_draw(ctx, tasks_list, plot_param, resource_list)

                # Arrows DRAW
                self.arrow_draw(ctx, tasks_list, predecessor_list, plot_param)

                report_surface.finish()
                img_str = base64.b64encode(buffered.getvalue())

                if img_str:
                    self.write({
                        'file_save': img_str,
                    })

            else:
                self.write({
                    'name': "Error: imposbile PDF",
                })

        else:
            raise UserError(_("You can't export pdf. Ask manager for permission."))




        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': self._name,
        #     'view_mode': 'form',
        #     'target': 'self',
        #     'res_id': self.id,
        # }



