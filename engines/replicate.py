from typing import List, Dict, Any

import replicate
from fastapi import HTTPException

from core.image_generator import ImageGenerator
from models.schemas import  EngineRequirement


class ReplicateGenerator(ImageGenerator):
    def __init__(self):
        super().__init__(
            name="Replicate",
            description="Replicate.com hosted models"
        )

    async def generate(self, params: Dict[str, Any], prompt: str, size: int, num_images: int) -> List[str]:
        if "api_token" not in params:
            raise HTTPException(status_code=400, detail="Replicate API token is required")

        try:
            client = replicate.Client(api_token=params["api_token"])
            model = params.get("model", "stability-ai/sdxl")

            # Configure for multiple images
            input_params = {
                "prompt": prompt,
                "width": size,
                "height": size,
                "num_outputs": num_images
            }

            response = await client.async_run(
                model,
                input=input_params
            )
            # In real implementation, convert URLs to base64
            return ["base64_encoded_image_data"] * num_images
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Replicate generation failed: {str(e)}")

    def get_required_params(self) -> List[EngineRequirement]:
        return [
            EngineRequirement(
                name="api_token",
                description="Replicate API token"
            ),
            EngineRequirement(
                name="model",
                description="Model identifier on Replicate"
            )
        ]