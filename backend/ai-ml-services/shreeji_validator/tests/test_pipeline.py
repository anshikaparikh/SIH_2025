from app.services.verification_pipeline import run_full_verification

def test_pipeline_runs():
    # Run pipeline on dummy path
    result = run_full_verification("dummy_path")
    
    # Check keys exist (values will come once ML/Blockchain are ready)
    assert "text" in result
    assert "anomaly_result" in result
    assert "blockchain_valid" in result
