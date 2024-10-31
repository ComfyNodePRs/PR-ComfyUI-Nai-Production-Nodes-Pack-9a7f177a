import numpy as np
import torch
from torch import Tensor
from PIL import Image, ImageEnhance, ImageFilter

def tensor2pil(image: Tensor) -> Image.Image:
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image: Image.Image) -> Tensor:
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class ImageContrast:
    CATEGORY = "image/postprocessing"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step":0.1})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_brightness"
    OUTPUT_NODE = True

    def apply_brightness(self, image, factor):
        pil_image = tensor2pil(image)
        #pil_image = pil_image.convert("RGB")
        pil_image = ImageEnhance.Contrast(pil_image).enhance(factor)
        pil_image = pil_image.convert("RGB")

        return (pil2tensor(pil_image),)

NODE_CLASS_MAPPINGS = {
    "Contrast Image": ImageContrast,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Contrast Image": "🌅Image Contrast",
}