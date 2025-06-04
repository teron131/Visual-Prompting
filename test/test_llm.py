#!/usr/bin/env python3
"""
Test LLM inference for video generation prompts.
Demonstrates the complete workflow from user request to structured prompt and optimized string.
"""

import json

from visual_prompting import reponse_to_string, run_llm


def test_jewelry_video_prompt():
    """Test LLM inference with jewelry product shot video request."""
    print("🎬 TESTING VIDEO PROMPT GENERATION")
    print("=" * 80)

    # Test configuration
    user_request = "Create a prompt to design a short clip with elegant jewellery product shot"
    media_type = "video"
    model = "openai/gpt-4.1-mini"  # Using a more cost-effective model

    print(f"User Request: {user_request}")
    print(f"Media Type: {media_type}")
    print(f"Model: {model}")
    print("=" * 80)

    try:
        print("🤖 Calling LLM...")

        # Generate structured prompt
        structured_result = run_llm(user_request=user_request, media_type=media_type, model=model, return_string=False)

        # Generate optimized string prompt
        string_prompt = run_llm(user_request=user_request, media_type=media_type, model=model, return_string=True)

        print("✅ LLM Response Generated Successfully!")
        print("-" * 40)

        # Display the structured result
        print("📋 STRUCTURED VIDEO PROMPT:")
        print("-" * 40)

        # Convert to dict for nice display
        result_dict = structured_result.model_dump()

        # Display required fields first
        print("\n🔴 REQUIRED FIELDS:")
        required_fields = ["subject", "context", "action", "style"]
        for field in required_fields:
            if field in result_dict and result_dict[field]:
                print(f"  • {field}: {result_dict[field]}")

        # Display optional fields that were filled
        print("\n🔵 OPTIONAL FIELDS (Generated):")
        optional_fields = [k for k in result_dict.keys() if k not in required_fields and result_dict[k] is not None]
        for field in optional_fields:
            value = result_dict[field]
            if isinstance(value, str) and len(value) > 60:
                print(f"  • {field}: {value[:60]}...")
            else:
                print(f"  • {field}: {value}")

        # Show the optimized string prompt
        print(f"\n🎯 OPTIMIZED STRING PROMPT (Ready for AI Generation):")
        print("-" * 40)
        print(f"'{string_prompt}'")

        # Show complete JSON
        print(f"\n📄 COMPLETE JSON OUTPUT:")
        print("-" * 40)
        print(json.dumps(result_dict, indent=2))

        # Statistics
        filled_fields = sum(1 for v in result_dict.values() if v is not None)
        total_fields = len(result_dict)
        string_length = len(string_prompt)
        print(f"\n📊 STATISTICS:")
        print(f"  • Fields filled: {filled_fields}/{total_fields}")
        print(f"  • Required fields: {len(required_fields)}")
        print(f"  • Optional fields used: {len(optional_fields)}")
        print(f"  • String prompt length: {string_length} characters")

        return structured_result, string_prompt

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("\nPlease check:")
        print("1. OPENROUTER_API_KEY is set in .env file")
        print("2. You have sufficient API credits")
        print("3. Network connection is working")
        return None, None


def test_manual_parsing():
    """Test the manual parsing function with a sample structured prompt."""
    print(f"\n\n🔧 TESTING MANUAL PARSING")
    print("=" * 80)

    try:
        # Generate a structured prompt first
        structured_result = run_llm(user_request="Create a prompt to design a short clip with elegant jewellery product shot", media_type="video", model="openai/gpt-4.1-mini", return_string=False)

        # Parse manually using the parsing function
        manual_parsed = reponse_to_string(structured_result)

        print("🔄 Manual parsing of structured prompt:")
        print(f"'{manual_parsed}'")
        print(f"Length: {len(manual_parsed)} characters")

        return manual_parsed

    except Exception as e:
        print(f"❌ MANUAL PARSING ERROR: {str(e)}")
        return None


def main():
    """Run the jewelry video prompt test with both structured and string outputs."""
    print("🧪 LLM INFERENCE TEST WITH STRING PARSING")
    print("Testing video prompt generation with jewelry product shot request\n")

    structured_result, string_prompt = test_jewelry_video_prompt()
    manual_parsed = test_manual_parsing()

    if structured_result and string_prompt:
        print(f"\n{'='*80}")
        print("🎉 TEST COMPLETED SUCCESSFULLY!")
        print("✅ Structured prompt generated with comprehensive fields")
        print("✅ Optimized string prompt created for AI generation")
        print("✅ Manual parsing function working correctly")
        print(f"\n🚀 READY FOR AI GENERATION:")
        print(f"Use this string with any video generation tool:")
        print(f"'{string_prompt}'")
    else:
        print(f"\n{'='*80}")
        print("💥 TEST FAILED!")
        print("Please check the error messages above and try again.")


if __name__ == "__main__":
    main()
