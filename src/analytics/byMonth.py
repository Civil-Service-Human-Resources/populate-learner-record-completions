import modules.analytics.AnalyticsService as AnalyticsService
data = AnalyticsService.get_analytics_by_month()
print(data.to_markdown())