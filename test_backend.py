#!/usr/bin/env python3
"""Quick test script for backend services"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("🧪 Testing backend imports...")

try:
    from app.config import get_settings
    print("✅ Config module imported")
    
    settings = get_settings()
    print(f"✅ Settings loaded: {settings.APP_NAME} v{settings.APP_VERSION}")
except Exception as e:
    print(f"❌ Config error: {e}")
    sys.exit(1)

try:
    from app.schemas import Text2ImageRequest, TaskResponse
    print("✅ Schemas module imported")
except Exception as e:
    print(f"❌ Schemas error: {e}")
    sys.exit(1)

try:
    from app.services.volcengine_service import MockVolcengineImageService
    print("✅ Services module imported")
    
    # Test mock service
    import asyncio
    async def test_mock():
        service = MockVolcengineImageService()
        result = await service.text_to_image("test prompt")
        return result
    
    result = asyncio.run(test_mock())
    if result.get("success"):
        print("✅ Mock service works")
    else:
        print("⚠️  Mock service returned non-success")
except Exception as e:
    print(f"❌ Services error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from app.routers import generate, task
    print("✅ Routers module imported")
except Exception as e:
    print(f"❌ Routers error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from app.main import app
    print("✅ Main app module imported")
    print(f"✅ App created: {app.title}")
except Exception as e:
    print(f"❌ Main app error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✨ All backend tests passed!")
print("🚀 Ready to start with: uvicorn app.main:app --reload")
