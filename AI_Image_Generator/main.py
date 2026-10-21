
import os
import io
import base64
import random
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from openai import (
    OpenAI,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    APIConnectionError,
    APITimeoutError,
    OpenAIError,
)
from PIL import Image

load_dotenv()

st.set_page_config(
    page_title="AI Image Studio Pro",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------- DESIGN -------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 80% 0%, #221742 0%, transparent 42%),
        radial-gradient(ellipse at 10% 80%, #0d2541 0%, transparent 45%),
        #080b15;
    color: #eef2ff;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #0e1222;
    border-right: 1px solid #293047;
}

.hero {
    padding: 35px 20px;
    text-align: center;
}

.hero h1 {
    font-size: clamp(2.3rem, 5vw, 4.2rem);
    font-weight: 800;
    letter-spacing: -2px;
    margin-bottom: 10px;
    background: linear-gradient(100deg, #67e8f9, #a78bfa, #f9a8d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #a8b3cc;
    font-size: 1.05rem;
}

.tag {
    display: inline-block;
    color: #c4b5fd;
    background: #30234d;
    border: 1px solid #58447f;
    border-radius: 30px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.panel {
    padding: 18px;
    background: rgba(25, 31, 53, .65);
    border: 1px solid #343b57;
    border-radius: 18px;
    margin-bottom: 15px;
}

.panel h3 {
    margin: 0 0 8px;
    color: #f1f5ff;
}

.panel p {
    color: #9aa9c7;
    margin: 0;
    font-size: 14px;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6366f1, #a855f7);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    min-height: 48px;
}

.stButton > button {
    border-radius: 11px;
    transition: all .2s ease;
}

.stButton > button:hover {
    border-color: #a78bfa;
    color: #c4b5fd;
}

[data-testid="stImage"] img {
    border-radius: 15px;
}

[data-testid="stMetric"] {
    background: #171d30;
    border: 1px solid #303a55;
    border-radius: 13px;
    padding: 12px;
}

textarea, input {
    border-radius: 12px !important;
}

.footer {
    text-align: center;
    color: #7986a4;
    font-size: 12px;
    padding-top: 35px;
}
</style>
""", unsafe_allow_html=True)

# ------------------- STATE -------------------

if "gallery" not in st.session_state:
    st.session_state.gallery = []

if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""

if "last_error" not in st.session_state:
    st.session_state.last_error = None

# ------------------- SETTINGS -------------------

SIZES = {
    "Square · 1:1": "1024x1024",
    "Portrait · 2:3": "1024x1536",
    "Landscape · 3:2": "1536x1024",
}

STYLES = {
    "📸 Photorealistic":
        "Photorealistic photography, natural textures, "
        "realistic lighting, fine details.",

    "🎬 Cinematic":
        "Cinematic composition, dramatic lighting, "
        "rich color grading, atmospheric depth.",

    "🌸 Anime":
        "High-quality anime illustration, expressive "
        "characters, vibrant colors, detailed backgrounds.",

    "🧊 3D Render":
        "High-end 3D rendering, detailed materials, "
        "global illumination, professional composition.",

    "🎨 Digital Art":
        "Beautiful digital painting, creative color palette, "
        "detailed brushwork, imaginative composition.",

    "🖌️ Watercolor":
        "Delicate watercolor painting, soft pigment washes, "
        "textured paper, artistic brush strokes.",

    "✏️ Pencil Sketch":
        "Detailed pencil drawing, graphite shading, "
        "expressive lines, traditional sketchbook style.",

    "✨ Fantasy":
        "Epic fantasy artwork, magical atmosphere, "
        "dramatic environment, intricate visual details.",

    "🎯 No Preset":
        "",
}

EXAMPLES = {
    "🏔️ Himalayan Future":
        "A futuristic city in Nepal surrounded by the "
        "Himalayan mountains, floating electric vehicles, "
        "beautiful architecture, golden sunset.",

    "🚀 Space Explorer":
        "An astronaut standing on an alien planet, "
        "two moons in the sky, glowing plants, "
        "vast cosmic landscape.",

    "🐉 Fantasy Dragon":
        "A majestic dragon flying over an ancient "
        "mountain kingdom, magical clouds, "
        "dramatic golden light.",

    "🏙️ Cyberpunk City":
        "A futuristic cyberpunk city at night, "
        "neon signs, rain-soaked streets, "
        "flying vehicles, atmospheric lighting.",
}

# ------------------- SIDEBAR -------------------

with st.sidebar:
    st.markdown("## 🎨 Image Studio")
    st.caption("PRO CREATIVE WORKSPACE")
    st.divider()

    st.markdown("### ⚙️ Generation Settings")

    size_label = st.selectbox(
        "Image aspect ratio",
        list(SIZES.keys()),
    )

    quality = st.selectbox(
        "Image quality",
        ["Low", "Medium", "High"],
        index=1,
    )

    style = st.selectbox(
        "Art style",
        list(STYLES.keys()),
    )

    enhance = st.toggle(
        "✨ Enhance prompt",
        value=True,
        help="Adds descriptive style and composition details.",
    )

    st.divider()

    st.markdown("### 🧪 Advanced Options")

    output_format = st.selectbox(
        "Output format",
        ["PNG", "JPEG", "WEBP"],
    )

    background = st.selectbox(
        "Background",
        ["Auto", "Opaque", "Transparent"],
    )

    if background == "Transparent" and output_format == "JPEG":
        st.warning(
            "JPEG does not support transparency. "
            "Choose PNG or WEBP."
        )

    st.divider()

    st.markdown("### 📊 Studio Statistics")
    st.metric("Images created", len(st.session_state.gallery))

    if st.button(
        "🗑️ Clear Gallery",
        use_container_width=True,
    ):
        st.session_state.gallery = []
        st.session_state.last_error = None
        st.rerun()

    st.divider()
    st.caption("Model: GPT Image 1")
    st.caption("Powered by OpenAI API")
    st.caption("Built with Python + Streamlit")

# ------------------- HEADER -------------------

st.markdown("""
<div class="hero">
    <span class="tag">AI POWERED CREATIVE STUDIO</span>
    <h1>Imagine it. Create it.</h1>
    <p>
        Transform your ideas into stunning visuals
        with the power of generative AI.
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------- WORKSPACE -------------------

left, right = st.columns([1, 1.15], gap="large")

with left:
    st.markdown("""
    <div class="panel">
        <h3>✍️ Create your masterpiece</h3>
        <p>Describe what you want to see. The more
        detail you provide, the better the result.</p>
    </div>
    """, unsafe_allow_html=True)

    st.text_area(
        "Your creative prompt",
        key="prompt_text",
        height=190,
        placeholder=(
            "A breathtaking futuristic city at sunset, "
            "glowing skyscrapers, cinematic lighting..."
        ),
    )

    st.markdown("#### 💡 Need inspiration?")

    example_names = list(EXAMPLES.keys())

    c1, c2 = st.columns(2)

    for index, name in enumerate(example_names):
        target = c1 if index % 2 == 0 else c2

        with target:
            if st.button(
                name,
                key=f"example_{index}",
                use_container_width=True,
            ):
                st.session_state.prompt_text = EXAMPLES[name]
                st.rerun()

    st.markdown("#### 🎛️ Current configuration")

    st.caption(
        f"Style: {style}  |  "
        f"Size: {size_label}  |  "
        f"Quality: {quality}"
    )

    generate = st.button(
        "✨ Generate Artwork",
        type="primary",
        use_container_width=True,
    )

with right:
    st.markdown("""
    <div class="panel">
        <h3>🖼️ Your canvas</h3>
        <p>Your generated artwork will appear here.
        Preview, save, and explore your creations.</p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------- GENERATION -------------------

    if generate:
        prompt = st.session_state.prompt_text.strip()
        api_key = os.getenv("OPENAI_API_KEY")

        if not prompt:
            st.warning("Please describe an image first.")

        elif not api_key or api_key.startswith("your_"):
            st.error(
                "API key is missing. Add OPENAI_API_KEY "
                "to your .env file."
            )

        elif background == "Transparent" and output_format == "JPEG":
            st.error(
                "Transparent backgrounds require PNG or WEBP."
            )

        else:
            final_prompt = prompt

            if enhance:
                final_prompt += (
                    "\n\nVisual style: "
                    + STYLES[style]
                    + "\nCreate a visually polished, "
                    "well-composed image."
                )

            try:
                client = OpenAI(
                    api_key=api_key,
                    timeout=180.0,
                    max_retries=1,
                )

                with st.spinner(
                    "🎨 Generating your masterpiece..."
                ):
                    result = client.images.generate(
                        model="gpt-image-1",
                        prompt=final_prompt,
                        size=SIZES[size_label],
                        quality=quality.lower(),
                        n=1,
                        output_format=output_format.lower(),
                        background=background.lower(),
                    )

                    encoded = result.data[0].b64_json

                    if not encoded:
                        raise ValueError(
                            "The API returned no image data."
                        )

                    raw_bytes = base64.b64decode(encoded)

                    image = Image.open(
                        io.BytesIO(raw_bytes)
                    )
                    image.load()

                    buffer = io.BytesIO()
                    image.save(
                        buffer,
                        format=output_format.upper(),
                    )

                    image_bytes = buffer.getvalue()

                st.session_state.gallery.insert(
                    0,
                    {
                        "id": datetime.now().strftime(
                            "%Y%m%d%H%M%S%f"
                        ),
                        "image": image_bytes,
                        "prompt": prompt,
                        "style": style,
                        "size": size_label,
                        "quality": quality,
                        "format": output_format,
                        "time": datetime.now().strftime(
                            "%d %b %Y · %H:%M"
                        ),
                    },
                )

                st.session_state.last_error = None
                st.success("✨ Artwork generated successfully!")

            except AuthenticationError:
                st.error(
                    "Invalid API key. Check your .env file."
                )

            except RateLimitError:
                st.error(
                    "Rate limit or API quota reached. "
                    "Check your OpenAI API usage and billing."
                )

            except BadRequestError as error:
                st.error(
                    f"Image request was rejected: {error.message}"
                )

            except (APIConnectionError, APITimeoutError):
                st.error(
                    "Connection problem or request timed out. "
                    "Please try again."
                )

            except OpenAIError as error:
                st.error(f"OpenAI API error: {error}")

            except Exception:
                st.error(
                    "An unexpected error occurred while "
                    "processing the image."
                )

    # ------------------- PREVIEW -------------------

    if st.session_state.gallery:
        latest = st.session_state.gallery[0]

        st.image(
            latest["image"],
            caption=latest["prompt"],
            use_container_width=True,
        )

        st.caption(
            f"{latest['style']} · "
            f"{latest['size']} · "
            f"{latest['time']}"
        )

        st.download_button(
            "⬇️ Download Artwork",
            data=latest["image"],
            file_name=(
                f"AI_Studio_{latest['id']}."
                f"{latest['format'].lower()}"
            ),
            mime=(
                "image/jpeg"
                if latest["format"] == "JPEG"
                else f"image/{latest['format'].lower()}"
            ),
            use_container_width=True,
            type="primary",
        )

    else:
        st.markdown("""
        <div style="
            min-height:330px;
            display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:column;
            border:2px dashed #3b4261;
            border-radius:20px;
            background:rgba(25,31,53,.35);
            text-align:center;
            padding:30px;
        ">
            <div style="font-size:55px">🪄</div>
            <h3>Your imagination starts here</h3>
            <p style="color:#9aa9c7">
                Enter a prompt and click Generate Artwork.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ------------------- GALLERY -------------------

st.divider()
st.markdown("## 🖼️ Your Creative Gallery")

if not st.session_state.gallery:
    st.info(
        "No artwork yet. Generate your first image "
        "to start building your gallery."
    )

else:
    st.caption(
        "Your gallery is stored during this browser session."
    )

    columns = st.columns(3)

    for index, item in enumerate(st.session_state.gallery):
        with columns[index % 3]:
            with st.container(border=True):
                st.image(
                    item["image"],
                    use_container_width=True,
                )

                st.markdown(
                    f"**{item['style']}**"
                )

                st.caption(item["prompt"][:110])
                st.caption(item["time"])

                st.download_button(
                    "⬇ Download",
                    data=item["image"],
                    file_name=(
                        f"artwork_{item['id']}."
                        f"{item['format'].lower()}"
                    ),
                    mime=(
                        "image/jpeg"
                        if item["format"] == "JPEG"
                        else f"image/{item['format'].lower()}"
                    ),
                    key=f"download_{item['id']}",
                    use_container_width=True,
                )

# ------------------- FOOTER -------------------

st.markdown("""
<div class="footer">
    AI IMAGE STUDIO PRO · Assignment #14
    <p>Made with Python, Streamlit & OpenAI</p>
</div>
""", unsafe_allow_html=True)
F