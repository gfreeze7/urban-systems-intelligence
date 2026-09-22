from src.database.connection import get_connection
from src.database.pipeline_runs import mark_stale_pipeline_runs


def test_mark_stale_pipeline_runs():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pipeline_runs (
                    pipeline_name,
                    started_at,
                    status
                )
                VALUES (
                    'pytest_stale_test',
                    CURRENT_TIMESTAMP - INTERVAL '1 hour',
                    'running'
                )
                RETURNING run_id
                """
            )

            run_id = cursor.fetchone()[0]

        connection.commit()

        stale_count = mark_stale_pipeline_runs(minutes=30)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT status, error_message
                FROM pipeline_runs
                WHERE run_id = %s
                """,
                (run_id,),
            )

            status, error_message = cursor.fetchone()

        assert stale_count >= 1
        assert status == "stale"
        assert error_message == "Run exceeded expected duration"

    finally:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM pipeline_runs
                WHERE pipeline_name = 'pytest_stale_test'
                """
            )

        connection.commit()
        connection.close()