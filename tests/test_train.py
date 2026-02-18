from src.models.train import ModelTrainer

def test_training_pipeline():
    trainer = ModelTrainer()
    rmse, r2 = trainer.train()

    assert rmse > 0
    assert 0 <= r2 <= 1
