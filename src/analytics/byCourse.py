import modules.analytics.AnalyticsService as AnalyticsService

data = AnalyticsService.get_analytics_by_course()
print(data.to_markdown())