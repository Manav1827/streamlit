import streamlit as st
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
from io import BytesIO
from paddleocr import PaddleOCR

# ========== Config ==========
st.set_page_config(page_title="🎨 Templates", layout="wide")
st.title("🎨 Template Gallery & Editor")

# ========== Template DB ==========
TEMPLATES = [
    {"title": "Classic Birthday Invite", "category": "Birthday Invitations", "file": "b1.png", "tag": "new"},
    {"title": "Fun Birthday Invite", "category": "Birthday Invitations", "file": "b2.png"},
    {"title": "Elegant Wedding Invitation", "category": "Wedding Invitations", "file": "w1.png", "tag": "featured"},
    {"title": "Floral Wedding Invite", "category": "Wedding Invitations", "file": "w2.png"},
    {"title": "Adventure Travel Reel", "category": "Travel Reels", "file": "t1.png"},
    {"title": "Travel Vlog Reel", "category": "Travel Reels", "file": "t2.png", "tag": "new"},
]

# ========== Functions ==========

def get_person_bbox_from_original(uploaded_file):
    uploaded_file.seek(0)
    result = remove(uploaded_file.read())
    img_rgba = Image.open(BytesIO(result)).convert("RGBA")
    alpha = np.array(img_rgba.split()[-1])
    mask = (alpha > 0).astype(np.uint8) * 255
    coords = cv2.findNonZero(mask)
    x, y, w, h = cv2.boundingRect(coords)
    return mask, (x, y, x + w, y + h)

def replace_person_with_user_mask_fit(template_file, user_file, resize_factor=1.0):
    template_file.seek(0)
    user_file.seek(0)
    original_img = Image.open(template_file).convert("RGB")
    original_np = np.array(original_img)
    person_mask, person_bbox = get_person_bbox_from_original(template_file)
    image_cv = cv2.cvtColor(original_np, cv2.COLOR_RGB2BGR)
    result_cleaned = cv2.inpaint(image_cv, person_mask, 3, cv2.INPAINT_TELEA)
    result_cleaned_rgb = cv2.cvtColor(result_cleaned, cv2.COLOR_BGR2RGB)
    user_cutout = remove(user_file.read())
    user_rgba = Image.open(BytesIO(user_cutout)).convert("RGBA")
    bbox_width = person_bbox[2] - person_bbox[0]
    bbox_height = person_bbox[3] - person_bbox[1]
    user_width, user_height = user_rgba.size
    base_scale = min(bbox_width / user_width, bbox_height / user_height) * 0.95
    final_scale = base_scale * resize_factor
    new_width = int(user_width * final_scale)
    new_height = int(user_height * final_scale)
    user_resized = user_rgba.resize((new_width, new_height), Image.Resampling.LANCZOS)
    mask_region = person_mask[person_bbox[1]:person_bbox[3], person_bbox[0]:person_bbox[2]]
    moments = cv2.moments(mask_region)
    cx = int(moments["m10"] / moments["m00"]) if moments["m00"] != 0 else bbox_width // 2
    cy = int(moments["m01"] / moments["m00"]) if moments["m00"] != 0 else bbox_height // 2
    paste_x = max(0, min(person_bbox[0] + cx - new_width // 2, original_img.width - new_width))
    paste_y = max(0, min(person_bbox[1] + cy - new_height // 2, original_img.height - new_height))
    background_cleaned = Image.fromarray(result_cleaned_rgb).convert("RGBA")
    final = background_cleaned.copy()
    final.paste(user_resized, (paste_x, paste_y), user_resized)
    return final.convert("RGB")

def detect_text_paddleocr(pil_image):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    result = ocr.ocr(img_bytes, cls=True)
    boxes = []
    for line in result:
        for box, (text, conf) in line:
            if conf >= 0.5 and text.strip() != "":
                x1, y1 = map(int, box[0])
                x2, y2 = map(int, box[2])
                boxes.append({"box": (x1, y1, x2, y2), "text": text})
    return boxes

def apply_text_edits(pil_image, text_boxes, user_inputs):
    img = pil_image.convert("RGBA")
    draw = ImageDraw.Draw(img)
    img_cv = np.array(pil_image.convert("RGB"))
    try:
        fallback_font = ImageFont.truetype("arial.ttf", 20)
    except:
        fallback_font = ImageFont.load_default()
    for idx, item in enumerate(text_boxes):
        x1, y1, x2, y2 = item["box"]
        replacement = user_inputs[idx]
        margin = 3
        x1c = max(0, x1 - margin)
        y1c = max(0, y1 - margin)
        x2c = min(img.width, x2 + margin)
        y2c = min(img.height, y2 + margin)
        outer_box = img_cv[y1c:y2c, x1c:x2c]
        parts = [outer_box[:margin, :], outer_box[-margin:, :], outer_box[:, :margin], outer_box[:, -margin:]]
        bg_pixels = np.vstack([arr.reshape(-1, 3) for arr in parts if arr.size > 0])
        avg_bg_color = tuple(np.mean(bg_pixels, axis=0).astype(int)) if bg_pixels.size > 0 else (255, 255, 255)
        inner_box = img_cv[y1:y2, x1:x2]
        gray_inner = cv2.cvtColor(inner_box, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray_inner, 180, 255, cv2.THRESH_BINARY_INV)
        mask_bool = mask > 0
        avg_text_color = tuple(np.mean(inner_box[mask_bool], axis=0).astype(int)) if np.any(mask_bool) else (0, 0, 0)
        draw.rectangle([x1, y1, x2, y2], fill=avg_bg_color)
        try:
            font = ImageFont.truetype("arial.ttf", size=y2 - y1)
        except:
            font = fallback_font
        draw.text((x1, y1), replacement, fill=avg_text_color, font=font)
    return img

# ========== UI Flow ==========

mode = st.radio("Choose Action", ["🖼️ Browse Templates", "✏️ Edit Selected Template"])

if mode == "🖼️ Browse Templates":
    st.subheader("📚 Template Gallery")
    search = st.text_input("Search templates...")
    cols = st.columns(3)
    for idx, t in enumerate([t for t in TEMPLATES if search.lower() in t["title"].lower()]):
        with cols[idx % 3]:
            st.image(f"assets/templates/{t['file']}", use_column_width=True)
            st.markdown(f"**{t['title']}**  \n*{t['category']}*")
            if st.button("⚡ Use Template", key=t['title']):
                path = os.path.join("assets/templates", t["file"])
                with open(path, "rb") as f:
                    st.session_state["template_file_bytes"] = f.read()
                    st.session_state["template_name"] = t["title"]
                st.success(f"✅ Template '{t['title']}' loaded for editing!")
                st.rerun()

elif mode == "✏️ Edit Selected Template":
    st.subheader("🎨 Edit Your Selected Template")

    # Load template from session or upload
    template_file = None
    if "template_file_bytes" in st.session_state:
        template_file = BytesIO(st.session_state["template_file_bytes"])
        st.info(f"🎯 Editing template: **{st.session_state.get('template_name', 'Template')}**")
    else:
        template_file = st.file_uploader("Upload Template Image")

    user_file = st.file_uploader("Upload Your Photo", type=["png", "jpg", "jpeg"])
    resize_factor = st.slider("Resize Person", 0.5, 2.0, 1.0)

    if template_file and user_file and st.button("🚀 Replace Person"):
        replaced_img = replace_person_with_user_mask_fit(template_file, user_file, resize_factor)
        st.session_state["replaced_img"] = replaced_img
        st.session_state["text_boxes"] = detect_text_paddleocr(replaced_img)
        st.success("✅ Person replaced!")

    if "replaced_img" in st.session_state and st.session_state["replaced_img"] is not None:
        st.image(st.session_state["replaced_img"], caption="🧑 Replaced Template", use_column_width=True)

        st.subheader("📝 Edit Text")
        user_inputs = []
        for idx, item in enumerate(st.session_state["text_boxes"]):
            val = st.text_input(f"Replace '{item['text']}'", key=f"text_{idx}")
            user_inputs.append(val if val.strip() else item["text"])

        if st.button("🎨 Generate Final Image"):
            final = apply_text_edits(st.session_state["replaced_img"], st.session_state["text_boxes"], user_inputs)
            st.image(final, caption="✅ Final Edited Image", use_column_width=True)
            buf = BytesIO()
            final.save(buf, format="PNG")
            st.download_button("📥 Download Final Image", data=buf.getvalue(), file_name="edited_template.png", mime="image/png")
    else:
        st.info("👈 Please upload both the template image and your image to start.")
        