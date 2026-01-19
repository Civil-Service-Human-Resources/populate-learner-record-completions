import modules.analytics.AnalyticsService as AnalyticsService

total_incomplete_records = AnalyticsService.get_total_incomplete_records()

by_month = AnalyticsService.get_analytics_by_month()
html_table_by_month = by_month.to_html()

by_course = AnalyticsService.get_analytics_by_course()
html_table_by_course = by_course.to_html()

html_template = open("analytics/analytics.tmp.html", "r").read()
html_template = html_template.replace("{{total_records}}", str(total_incomplete_records))
html_template = html_template.replace("{{by_month_table}}", html_table_by_month)
html_template = html_template.replace("{{by_course_table}}", html_table_by_course)

with open("/app-data/analytics.html", "w") as html_file:
    html_file.write(html_template)
