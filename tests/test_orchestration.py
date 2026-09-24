import pytest

import src.orchestration.pipeline as pipeline


def test_pipeline_records_failure(monkeypatch):
    finished_runs = []

    monkeypatch.setattr(
        pipeline,
        "mark_stale_pipeline_runs",
        lambda: 0,
    )

    monkeypatch.setattr(
        pipeline,
        "start_pipeline_run",
        lambda pipeline_name: 999,
    )

    def fail_census_stage():
        raise RuntimeError("Controlled orchestration failure")

    monkeypatch.setattr(
        pipeline,
        "run_census_stage",
        fail_census_stage,
    )

    def capture_finish(run_id, status, **kwargs):
        finished_runs.append(
            {
                "run_id": run_id,
                "status": status,
                **kwargs,
            }
        )

    monkeypatch.setattr(
        pipeline,
        "finish_pipeline_run",
        capture_finish,
    )

    with pytest.raises(
        RuntimeError,
        match="Controlled orchestration failure",
    ):
        pipeline.run_pipeline()

    assert len(finished_runs) == 1
    assert finished_runs[0]["run_id"] == 999
    assert finished_runs[0]["status"] == "failed"
    assert (
        finished_runs[0]["error_message"]
        == "Controlled orchestration failure"
    )


def test_pipeline_records_success(monkeypatch):
    finished_runs = []

    monkeypatch.setattr(
        pipeline,
        "mark_stale_pipeline_runs",
        lambda: 0,
    )

    monkeypatch.setattr(
        pipeline,
        "start_pipeline_run",
        lambda pipeline_name: 1000,
    )

    monkeypatch.setattr(
        pipeline,
        "run_census_stage",
        lambda: {
            "inserted": 2,
            "updated": 3,
            "unchanged": 194,
        },
    )

    monkeypatch.setattr(
        pipeline,
        "run_bnia_stage",
        lambda: None,
    )

    monkeypatch.setattr(
        pipeline,
        "run_geography_stage",
        lambda: None,
    )

    def capture_finish(run_id, status, **kwargs):
        finished_runs.append(
            {
                "run_id": run_id,
                "status": status,
                **kwargs,
            }
        )

    monkeypatch.setattr(
        pipeline,
        "finish_pipeline_run",
        capture_finish,
    )

    results = pipeline.run_pipeline()

    assert results["census"]["inserted"] == 2
    assert results["census"]["updated"] == 3
    assert results["census"]["unchanged"] == 194

    assert len(finished_runs) == 1
    assert finished_runs[0]["run_id"] == 1000
    assert finished_runs[0]["status"] == "success"

    assert finished_runs[0]["records_received"] == 199
    assert finished_runs[0]["records_processed"] == 5
    assert finished_runs[0]["records_inserted"] == 2
    assert finished_runs[0]["records_updated"] == 3
    assert finished_runs[0]["records_unchanged"] == 194