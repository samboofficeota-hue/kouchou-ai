from copy import deepcopy

import pytest

from src.schemas.report import ReportVisibility
from src.services.report_status import convert_old_format_status


# FIXME: report_status.jsonのフォーマット変更に対応するための関数のテストコード。広聴AIをver3.0にした段階で削除する。
# https://github.com/digitaldemocracy2030/kouchou-ai/issues/507
class TestReportStatus:
    """レポートステータス関連のテスト"""

    @pytest.fixture
    def old_format_public_data(self):
        """is_public: trueを持つ旧形式のデータ"""
        return {
            "test-slug": {
                "slug": "test-slug",
                "status": "ready",
                "title": "テストタイトル",
                "description": "テスト説明",
                "is_pubcom": True,
                "created_at": "2025-05-13T07:56:58.405239+00:00",
                "is_public": True,
            }
        }

    @pytest.fixture
    def old_format_private_data(self):
        """is_public: falseを持つ旧形式のデータ"""
        return {
            "test-slug": {
                "slug": "test-slug",
                "status": "ready",
                "title": "テストタイトル",
                "description": "テスト説明",
                "is_pubcom": True,
                "created_at": "2025-05-13T07:56:58.405239+00:00",
                "is_public": False,
            }
        }

    @pytest.fixture
    def new_format_data(self):
        """visibilityを持つ新形式のデータ"""
        return {
            "test-slug": {
                "slug": "test-slug",
                "status": "ready",
                "title": "テストタイトル",
                "description": "テスト説明",
                "is_pubcom": True,
                "visibility": "unlisted",
                "created_at": "2025-05-13T07:56:58.405239+00:00",
            }
        }

    @pytest.fixture
    def mixed_format_data(self):
        """旧形式と新形式が混在したデータ"""
        return {
            "old-slug": {
                "slug": "old-slug",
                "status": "ready",
                "title": "旧形式タイトル",
                "description": "旧形式説明",
                "is_pubcom": True,
                "created_at": "2025-05-13T07:56:58.405239+00:00",
                "is_public": True,
            },
            "new-slug": {
                "slug": "new-slug",
                "status": "ready",
                "title": "新形式タイトル",
                "description": "新形式説明",
                "is_pubcom": True,
                "visibility": "unlisted",
                "created_at": "2025-05-13T07:56:58.405239+00:00",
            },
        }

    def test_convert_is_public_true_to_visibility_public(self, old_format_public_data):
        """is_public: trueをvisibility: publicに変換するテスト"""
        # 入力データのコピーを作成して元のデータが変更されないようにする
        input_data = deepcopy(old_format_public_data)

        # 関数を実行
        result = convert_old_format_status(input_data)

        # 結果を検証
        assert "test-slug" in result
        assert "visibility" in result["test-slug"]
        assert result["test-slug"]["visibility"] == ReportVisibility.PUBLIC.value
        assert "is_public" not in result["test-slug"]

    def test_convert_is_public_false_to_visibility_private(self, old_format_private_data):
        """is_public: falseをvisibility: privateに変換するテスト"""
        # 入力データのコピーを作成して元のデータが変更されないようにする
        input_data = deepcopy(old_format_private_data)

        # 関数を実行
        result = convert_old_format_status(input_data)

        # 結果を検証
        assert "test-slug" in result
        assert "visibility" in result["test-slug"]
        assert result["test-slug"]["visibility"] == ReportVisibility.PRIVATE.value
        assert "is_public" not in result["test-slug"]

    def test_new_format_data_unchanged(self, new_format_data):
        """既に新形式になっているデータは変更されないことを確認するテスト"""
        # 入力データのコピーを作成して元のデータが変更されないようにする
        input_data = deepcopy(new_format_data)
        original_visibility = input_data["test-slug"]["visibility"]

        # 関数を実行
        result = convert_old_format_status(input_data)

        # 結果を検証
        assert "test-slug" in result
        assert "visibility" in result["test-slug"]
        assert result["test-slug"]["visibility"] == original_visibility
        assert "is_public" not in result["test-slug"]

    def test_empty_dict(self):
        """空の辞書を渡した場合のテスト"""
        # 空の辞書を渡す
        input_data = {}

        # 関数を実行
        result = convert_old_format_status(input_data)

        # 結果を検証
        assert result == {}

    def test_mixed_format_data(self, mixed_format_data):
        """旧形式と新形式が混在したデータのテスト"""
        # 入力データのコピーを作成して元のデータが変更されないようにする
        input_data = deepcopy(mixed_format_data)
        original_new_visibility = input_data["new-slug"]["visibility"]

        # 関数を実行
        result = convert_old_format_status(input_data)

        # 結果を検証
        # 旧形式のデータが変換されていることを確認
        assert "old-slug" in result
        assert "visibility" in result["old-slug"]
        assert result["old-slug"]["visibility"] == ReportVisibility.PUBLIC.value
        assert "is_public" not in result["old-slug"]

        # 新形式のデータが変更されていないことを確認
        assert "new-slug" in result
        assert "visibility" in result["new-slug"]
        assert result["new-slug"]["visibility"] == original_new_visibility
        assert "is_public" not in result["new-slug"]
