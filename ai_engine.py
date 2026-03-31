import google.generativeai as genai
import json

SYSTEM_PROMPT = """You are an expert technical inspector and report generation AI.
Your task is to merge data from an Inspection Report and a Thermal Report to create a highly professional, structured Main Detailed Diagnostic Report (DDR).

Output strictly in JSON format matching this structure:
{
  "property_issue_summary": "Brief overall summary.",
  "probable_root_cause": "Overall likely root causes derived from the data.",
  "severity_assessment": {
    "level": "Low/Medium/High/Critical",
    "reasoning": "Explanation for severity."
  },
  "recommended_actions": ["Action 1", "Action 2"],
  "additional_notes": "Any other relevant notes or 'Not Available'.",
  "missing_or_unclear_information": ["Missing details here, or 'Not Available'"],
  "area_observations": [
    {
      "area_name": "Name of the area (e.g., Roof, HVAC)",
      "observation": "Detailed observation logically combining inspection and thermal findings.",
      "related_images": ["exact_image_id_1", "exact_image_id_2"]
    }
  ]
}

CRITICAL RULES:
- Do NOT invent facts. If information is missing or conflicting, state "Not Available" or explain the conflict.
- Use simple, client-friendly language, avoiding unnecessary jargon.
- I will provide you with the extracted text from both reports.
- I will also provide you with the extracted images. Each image will be preceded by its EXACT ID (e.g. 'inspection_img_1').
- Use these exact IDs in the 'related_images' array for the corresponding observation.
- If an expected image for an observation is missing, explicitly mention "Image Not Available" in the observation text itself.
- Ensure no duplicate points.
"""

def generate_ddr_report(api_key, inspection_text, inspection_images, thermal_text, thermal_images):
    """
    Calls the Gemini API to generate the structured DDR Report.
    """
    if api_key.strip().lower() == "demo":
        import time
        time.sleep(2) # Simulate processing time
        
        ins_id = inspection_images[0]['id'] if inspection_images else "none"
        th_id = thermal_images[0]['id'] if thermal_images else "none"
        
        related_ids = []
        if ins_id != "none": related_ids.append(ins_id)
        if th_id != "none": related_ids.append(th_id)
        
        return {
            "property_issue_summary": "DEMO MODE: Widespread moisture intrusion in the upper facility.",
            "probable_root_cause": "DEMO MODE: Failed flashing on the main roof.",
            "severity_assessment": {
                "level": "High",
                "reasoning": "DEMO MODE: High moisture levels shown in thermal anomalies."
            },
            "recommended_actions": ["DEMO MODE: Replace flashing", "DEMO MODE: Dehumidify area"],
            "additional_notes": "This is a simulated demo report because no API Key was provided.",
            "missing_or_unclear_information": ["Exact area square footage Not Available"],
            "area_observations": [
                {
                    "area_name": "Main Roof Structure (DEMO)",
                    "observation": "Extracted text indicates water pooling. Thermal imaging confirms exact cold spots indicating active leakage.",
                    "related_images": related_ids
                }
            ]
        }

    genai.configure(api_key=api_key)
    
    # We use gemini-1.5-pro because it has standard multimodal capabilities and large context
    model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                                  system_instruction=SYSTEM_PROMPT)
    
    prompt_parts = []
    
    # Add text
    prompt_parts.append("=== INSPECTION REPORT TEXT ===\n" + inspection_text + "\n")
    prompt_parts.append("=== THERMAL REPORT TEXT ===\n" + thermal_text + "\n")
    
    # Add Inspection Images with IDs
    prompt_parts.append("\n=== INSPECTION REPORT IMAGES ===\n")
    if not inspection_images:
         prompt_parts.append("No images extracted.\n")
    for img_dict in inspection_images:
         prompt_parts.append(f"Image ID: {img_dict['id']}")
         prompt_parts.append(img_dict["image"])
         
    # Add Thermal Images with IDs
    prompt_parts.append("\n=== THERMAL REPORT IMAGES ===\n")
    if not thermal_images:
         prompt_parts.append("No images extracted.\n")
    for img_dict in thermal_images:
         prompt_parts.append(f"Image ID: {img_dict['id']}")
         prompt_parts.append(img_dict["image"])
         
    prompt_parts.append("\nNow generate the JSON DDR Report following the System rules:")
    
    # Call the model
    # We force JSON format in generation config
    try:
         response = model.generate_content(
             prompt_parts,
             generation_config={"response_mime_type": "application/json"}
         )
         return json.loads(response.text)
    except Exception as e:
         print(f"Error calling Gemini: {e}")
         # Attempt fallback without forced JSON
         fallback_response = model.generate_content(prompt_parts)
         
         # simplistic cleanup
         t = fallback_response.text.strip()
         if t.startswith("```json"):
             t = t[7:]
         if t.endswith("```"):
             t = t[:-3]
         return json.loads(t)
