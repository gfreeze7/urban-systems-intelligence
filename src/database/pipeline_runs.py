from src.database.connection import get_connection


def start_pipeline_run(pipeline_name):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pipeline_runs (
                    pipeline_name,
                    status
                )
                VALUES (%s, %s)
                RETURNING run_id
                """,
                (
                    pipeline_name,
                    "running",
                ),
            )

            run_id = cursor.fetchone()[0]

        connection.commit()
        return run_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def finish_pipeline_run(
    run_id,
    status,
    records_processed=None,
    error_message=None,
    records_received=None,
    records_inserted=None,
    records_updated=None,
    records_unchanged=None,
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE pipeline_runs
                SET
                    finished_at = CURRENT_TIMESTAMP,
                    status = %s,
                    records_processed = %s,
                    error_message = %s,
                    records_received = %s,
                    records_inserted = %s,
                    records_updated = %s,
                    records_unchanged = %s
                WHERE run_id = %s
                """,
                (
                    status,
                    records_processed,
                    error_message,
                    records_received,
                    records_inserted,
                    records_updated,
                    records_unchanged,
                    run_id,
                ),
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def mark_stale_pipeline_runs(minutes=30):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE pipeline_runs
                SET
                    finished_at = CURRENT_TIMESTAMP,
                    status = 'stale',
                    error_message = 'Run exceeded expected duration'
                WHERE status = 'running'
                  AND started_at < CURRENT_TIMESTAMP - (%s * INTERVAL '1 minute')
                RETURNING run_id
                """,
                (minutes,),
            )

            stale_runs = cursor.fetchall()

        connection.commit()

        return len(stale_runs)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()