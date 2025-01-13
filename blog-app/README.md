# blog-app

## setup
### 前提
poetryをインストールおいてください

### コマンド
```bash
poetry shell
cd blog-app
python scripts/create_table.py # tableを追加する
uvicorn main:app --reload
```

## テスト
### pytest
```
pytest .
```
### coverage
```
pytest --cov=.
```