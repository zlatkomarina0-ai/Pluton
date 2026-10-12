"""Tests for Phase 3 Sync Engine"""
import pytest
import asyncio
from app.phase3.sync_engine import SyncEngine

@pytest.fixture
async def sync_engine():
    engine = SyncEngine("postgresql://test:test@localhost:5432/pluton_test")
    yield engine

@pytest.mark.asyncio
async def test_sync_entity_basic(sync_engine):
    """Test basic entity sync"""
    result = await sync_engine.sync_entity(
        entity_type="fixture",
        entity_id=1,
        data={"status": "scheduled", "date": "2026-10-15"}
    )
    assert result is True

@pytest.mark.asyncio
async def test_sync_queue_not_empty(sync_engine):
    """Test sync queue has items"""
    await sync_engine.sync_entity("team", 5, {"name": "Test Team"})
    assert not sync_engine.sync_queue.empty()
