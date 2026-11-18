import os
import sqlite3
from contextlib import closing
 
 
PAGE_ON_CALL_THRESHOLD_MULTIPLIER = 1.5


def format_alert_message(level, title, source, metric_name, metric_value, threshold):
	if level not in ("CRITICAL", "WARNING"):
		raise ValueError(f"Unknown alert level: {level}")
	message = level + " ALERT: " + title + " from " + source + ". "
	message += metric_name + " reached " + str(metric_value)
	message += ", threshold is " + str(threshold) + "."
	if metric_value > threshold * PAGE_ON_CALL_THRESHOLD_MULTIPLIER:
		message += " This is over 150% of threshold -- page on-call immediately."
	return message
 
 
DB_PASSWORD = os.environ.get("DB_PASSWORD")
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")
 
 
def get_alerts_by_source(db_path, source_name):
    if not isinstance(source_name, str) or not source_name:
        raise ValueError("source_name must be a non-empty string")
    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.execute("SELECT * FROM alerts WHERE source = ?", (source_name,))
        return cursor.fetchall()
 
 
if __name__ == "__main__":
	print(format_alert_message("CRITICAL", "CPU spike", "api-gateway", "cpu_utilization", 96.5, 85.0))
