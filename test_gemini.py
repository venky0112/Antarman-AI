"""
Test script for Gemini LLM integration
Run this to verify Gemini is configured and working properly
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

def test_gemini_basic():
    """Test basic Gemini connection and response"""
    print("=" * 60)
    print("Testing Google Gemini Integration")
    print("=" * 60)
    
    from backend.llm_agent import get_llm_response
    
    # Single-prompt mode: read prompt from argv or stdin to save tokens
    import sys
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:]).strip()
    else:
        try:
            prompt = input('\nEnter a single test prompt (or press Enter to use default): ').strip()
        except EOFError:
            prompt = ""

    if not prompt:
        prompt = "I'm feeling really anxious today"

    print(f"\n[Test] Input: {prompt}")
    print("-" * 60)
    try:
        # Pass minimal history for token savings
        response = get_llm_response(prompt, conversation_history=None)
        print(f"✓ Response:\n{response}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    return True


def test_gemini_multi_turn():
    """Test multi-turn conversation"""
    print("\n" + "=" * 60)
    print("Testing Multi-Turn Conversation")
    print("=" * 60)
    
    from backend.llm_agent import get_llm_response
    
    history = []
    messages = [
        "I'm feeling stressed",
        "Can you suggest a breathing exercise?",
        "That helped, thank you",
    ]
    
    for i, msg in enumerate(messages, 1):
        print(f"\n[Turn {i}] User: {msg}")
        print("-" * 60)
        
        try:
            response = get_llm_response(msg, history)
            print(f"Assistant: {response}")
            
            # Update history
            history.append({"role": "user", "content": msg})
            history.append({"role": "assistant", "content": response})
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    print("\n" + "=" * 60)
    print("✓ Multi-turn conversation test passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    # Check for API key
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        print("❌ ERROR: GEMINI_API_KEY not found in backend/.env")
        print("   Get your key from: https://ai.google.dev/metrics/explorer")
        sys.exit(1)
    
    print(f"✓ GEMINI_API_KEY found ({gemini_key[:20]}...)")
    
    # Run tests. By default only run single-prompt basic test to save tokens.
    try:
        # Optional: pass --multi to also run multi-turn test
        multi = False
        if "--multi" in sys.argv:
            multi = True
            # remove flag so prompt parsing isn't affected
            sys.argv = [a for a in sys.argv if a != "--multi"]

        if test_gemini_basic() and multi:
            test_gemini_multi_turn()
    except KeyboardInterrupt:
        print("\n\nTests interrupted.")
        sys.exit(1)
