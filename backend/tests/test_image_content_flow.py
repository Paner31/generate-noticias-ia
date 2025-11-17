"""
Test to verify image content flows correctly from task -> Redis -> API -> Frontend
"""
import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import redis
from datetime import datetime
from app.core.config import settings
from app.core.tasks import _save_job_to_redis, _get_job_from_redis


def test_redis_serialization_with_image_fields():
    """Test that image fields are properly saved to and retrieved from Redis"""

    # Create test job data with image fields
    job_id = "test-job-123"
    job_data = {
        "job_id": job_id,
        "status": "completed",
        "progress": 100,
        "notes": [
            {
                "note_id": "test-note-1",
                "content": "Test article content",
                "sources": ["https://example.com"],
                "tokens_used": 1000,
                "model": "deepseek/deepseek-chat",
                "image_prompt": "A futuristic scene with AI and doctors",
                "instagram_copy": "Check out this amazing AI news! 🤖 #AI #Tech",
                "facebook_copy": "Did you know AI can now diagnose diseases?",
                "linkedin_copy": "AI is revolutionizing healthcare diagnostics."
            }
        ],
        "error": None,
        "created_at": datetime.utcnow(),
        "completed_at": datetime.utcnow()
    }

    # Save to Redis
    _save_job_to_redis(job_id, job_data)

    # Retrieve from Redis
    retrieved_data = _get_job_from_redis(job_id)

    # Verify all fields are present
    assert retrieved_data is not None, "Job data should be retrievable from Redis"
    assert retrieved_data["job_id"] == job_id
    assert retrieved_data["status"] == "completed"
    assert len(retrieved_data["notes"]) == 1

    note = retrieved_data["notes"][0]
    assert note["note_id"] == "test-note-1"
    assert note["content"] == "Test article content"

    # CRITICAL: Verify image fields are present
    assert "image_prompt" in note, "image_prompt field should be in Redis"
    assert note["image_prompt"] == "A futuristic scene with AI and doctors"

    assert "instagram_copy" in note, "instagram_copy field should be in Redis"
    assert note["instagram_copy"] == "Check out this amazing AI news! 🤖 #AI #Tech"

    assert "facebook_copy" in note, "facebook_copy field should be in Redis"
    assert note["facebook_copy"] == "Did you know AI can now diagnose diseases?"

    assert "linkedin_copy" in note, "linkedin_copy field should be in Redis"
    assert note["linkedin_copy"] == "AI is revolutionizing healthcare diagnostics."

    # Cleanup
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    redis_client.delete(f"job:{job_id}")

    print("✓ Redis serialization test PASSED - All image fields preserved")


def test_api_response_schema():
    """Test that the API response schema includes image fields"""
    from app.models.schemas import GeneratedNote, JobStatusResponse
    from pydantic import ValidationError

    # Create a GeneratedNote with all image fields
    note_data = {
        "note_id": "test-note-1",
        "content": "Test content",
        "sources": ["https://example.com"],
        "tokens_used": 1000,
        "model": "test-model",
        "image_prompt": "Test image prompt",
        "instagram_copy": "Test instagram",
        "facebook_copy": "Test facebook",
        "linkedin_copy": "Test linkedin"
    }

    # This should not raise ValidationError
    try:
        note = GeneratedNote(**note_data)
        assert note.image_prompt == "Test image prompt"
        assert note.instagram_copy == "Test instagram"
        assert note.facebook_copy == "Test facebook"
        assert note.linkedin_copy == "Test linkedin"
        print("✓ Schema validation test PASSED - GeneratedNote accepts image fields")
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e}")

    # Test JobStatusResponse includes notes with image fields
    job_response_data = {
        "job_id": "test-job",
        "status": "completed",
        "progress": 100,
        "notes": [note_data],
        "created_at": datetime.utcnow()
    }

    try:
        response = JobStatusResponse(**job_response_data)
        assert len(response.notes) == 1
        assert response.notes[0].image_prompt == "Test image prompt"
        print("✓ Schema validation test PASSED - JobStatusResponse preserves image fields")
    except ValidationError as e:
        raise AssertionError(f"JobStatusResponse validation failed: {e}")


def test_json_serialization():
    """Test that image fields survive JSON serialization/deserialization"""
    note_dict = {
        "note_id": "test-1",
        "content": "Content",
        "sources": ["https://example.com"],
        "tokens_used": 100,
        "model": "test",
        "image_prompt": "Image prompt with émojis 🎨",
        "instagram_copy": "Instagram with émojis 📱",
        "facebook_copy": "Facebook post",
        "linkedin_copy": "LinkedIn post"
    }

    # Serialize to JSON
    json_str = json.dumps(note_dict)

    # Deserialize from JSON
    restored_dict = json.loads(json_str)

    # Verify all image fields are present
    assert "image_prompt" in restored_dict
    assert "instagram_copy" in restored_dict
    assert "facebook_copy" in restored_dict
    assert "linkedin_copy" in restored_dict

    # Verify values match (including emojis)
    assert restored_dict["image_prompt"] == note_dict["image_prompt"]
    assert restored_dict["instagram_copy"] == note_dict["instagram_copy"]

    print("✓ JSON serialization test PASSED - Image fields survive JSON round-trip")


if __name__ == "__main__":
    print("Running image content flow tests...\n")

    print("Test 1: Redis Serialization")
    test_redis_serialization_with_image_fields()
    print()

    print("Test 2: API Response Schema")
    test_api_response_schema()
    print()

    print("Test 3: JSON Serialization")
    test_json_serialization()
    print()

    print("=" * 60)
    print("All tests PASSED! ✓")
    print("=" * 60)
