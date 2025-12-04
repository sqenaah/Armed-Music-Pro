import random
from pathlib import Path
import aiohttp
from aiohttp import client_exceptions
import hashlib
import asyncio

class UnableToFetchCarbon(Exception):
    pass

THEMES = [
    "3024-night","a11y-dark","blackboard","base16-dark","base16-light",
    "cobalt","duotone-dark","dracula-pro","hopscotch","lucario",
    "material","monokai","nightowl","nord","oceanic-next",
    "one-light","one-dark","panda-syntax","parasio-dark","seti",
    "shades-of-purple","solarized+dark","solarized+light","synthwave-84",
    "twilight","verminal","vscode","yeti","zenburn"
]

COLORS = [
    "#FF0000","#FF5733","#FFFF00","#008000","#0000FF","#800080",
    "#A52A2A","#FF00FF","#D2B48C","#00FFFF","#808000","#800000",
    "#30D5C8","#00FF00","#008080","#4B0082","#EE82EE","#FFC0CB",
    "#000000","#FFFFFF","#808080"
]

class CarbonAPI:
    def __init__(
        self,
        language="auto",
        drop_shadow=True,
        drop_shadow_blur="68px",
        drop_shadow_offset="20px",
        drop_shadow_color="rgba(0,0,0,0.5)",
        font_family="JetBrains Mono",
        font_size=20,
        watermark=False,
        cache_dir="cache",
        transparent_background=False,
        padding_per_line=10,
        min_padding=20,
        max_padding=100,
        char_width=10,
        line_height=20,
        horizontal_padding=20,
        max_width=1200,
        device_width=None,
        gradient=True
    ):
        self.language=language
        self.drop_shadow=drop_shadow
        self.drop_shadow_blur=drop_shadow_blur
        self.drop_shadow_offset=drop_shadow_offset
        self.drop_shadow_color=drop_shadow_color
        self.font_family=font_family
        self.font_size=font_size
        self.watermark=watermark
        self.transparent_background=transparent_background
        self.padding_per_line=padding_per_line
        self.min_padding=min_padding
        self.max_padding=max_padding
        self.char_width=char_width
        self.line_height=line_height
        self.horizontal_padding=horizontal_padding
        self.max_width=max_width
        self.device_width=device_width or max_width
        self.gradient=gradient
        self.cache_dir=Path(cache_dir)
        self.cache_dir.mkdir(parents=True,exist_ok=True)

    def _generate_cache_name(self,text,user_id,theme,color):
        hash_digest=hashlib.md5(text.encode()).hexdigest()
        return self.cache_dir / f"carbon_{user_id}_{hash_digest}_{theme}_{color}.png"

    def _calculate_vertical_padding(self,text):
        lines=text.count('\n')+1
        padding=lines*self.padding_per_line
        padding=max(self.min_padding,min(padding,self.max_padding))
        return f"{padding}px"

    def _calculate_width(self,text,font_size):
        max_line=max(text.split('\n'),key=len,default='')
        width=len(max_line)*self.char_width*font_size//20+self.horizontal_padding*2
        return min(width,self.device_width)

    def _adjust_font_size(self,text):
        max_line=max(text.split('\n'),key=len,default='')
        required_width=len(max_line)*self.char_width+self.horizontal_padding*2
        if required_width<=self.device_width:
            return self.font_size
        scale=self.device_width/required_width
        return max(8,int(self.font_size*scale))

    def _get_background(self,color):
        if self.gradient:
            return f"linear-gradient(135deg,{color}33,{color}AA)"
        return color

    async def generate(self,text,user_id,theme=None,background_color=None,smart_size=True,auto_font=True,adaptive=True):
        theme_choice=theme or random.choice(THEMES)
        color_choice=background_color or random.choice(COLORS)
        file_path=self._generate_cache_name(text,user_id,theme_choice,color_choice)
        if file_path.exists():
            return str(file_path.resolve())
        font_size=self.font_size
        if auto_font and smart_size:
            font_size=self._adjust_font_size(text)
        payload={
            "code":text,
            "backgroundColor":"rgba(0,0,0,0)" if self.transparent_background else self._get_background(color_choice),
            "theme":theme_choice,
            "dropShadow":self.drop_shadow,
            "dropShadowOffsetY":self.drop_shadow_offset,
            "dropShadowBlurRadius":self.drop_shadow_blur,
            "dropShadowColor":self.drop_shadow_color,
            "fontFamily":self.font_family,
            "language":self.language,
            "watermark":self.watermark,
            "fontSize":f"{font_size}px",
            "widthAdjustment":not smart_size,
            "paddingVertical":self._calculate_vertical_padding(text),
            "paddingHorizontal":f"{self.horizontal_padding}px"
        }
        if smart_size:
            payload["backgroundWidth"]=self._calculate_width(text,font_size)
        if adaptive:
            payload["backgroundWidth"]=min(payload["backgroundWidth"],self.device_width)
        async with aiohttp.ClientSession(headers={"Content-Type":"application/json"}) as session:
            try:
                async with session.post("https://carbonara.solopov.dev/api/cook",json=payload) as resp:
                    if resp.status!=200:
                        raise UnableToFetchCarbon(f"Ошибка API:{resp.status}")
                    data=await resp.read()
            except client_exceptions.ClientConnectorError:
                raise UnableToFetchCarbon("Не удалось подключиться к серверу Carbon.")
        file_path.write_bytes(data)
        return str(file_path.resolve())

    async def generate_multiple(self,code_list,user_ids,themes=None,colors=None,smart_size=True,auto_font=True,adaptive=True):
        tasks=[]
        for i,code in enumerate(code_list):
            theme_choice=themes[i] if themes and i<len(themes) else None
            color_choice=colors[i] if colors and i<len(colors) else None
            tasks.append(self.generate(code,user_ids[i],theme=theme_choice,background_color=color_choice,smart_size=smart_size,auto_font=auto_font,adaptive=adaptive))
        return await asyncio.gather(*tasks)