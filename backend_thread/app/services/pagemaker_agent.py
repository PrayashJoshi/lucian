# app/services/pagemaker_agent.py

import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..utils.logger import get_logger
import aiofiles  # Import aiofiles

logger = get_logger(__name__)

class PagemakerAgent:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'xml', 'jinja'])
        )
        self.output_dir = os.path.join(os.getcwd(), 'frontend', 'src', 'components', 'generated')

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"PagemakerAgent initialized. Output directory: {self.output_dir}")

    async def generate_vue_component(self, component_name: str, data: dict) -> str:
        """
        Generate a Vue component file based on the provided data.
        """
        try:
            template = self.env.get_template('vue_component.jinja')
            rendered = template.render(component_name=component_name, data=data)
            file_path = os.path.join(self.output_dir, f"{component_name}.vue")
            async with aiofiles.open(file_path, 'w') as f:
                await f.write(rendered)
            logger.info(f"Generated Vue component: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error in generating Vue component: {e}")
            return ""
