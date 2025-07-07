# import streamlit as st

# st.title("🖼️ Templates")

# categories = ["Birthday", "Wedding", "Travel", "Promo", "Baby Shower"]
# category = st.selectbox("Select Category", categories)

# st.subheader(f"{category} Templates")

# st.image("https://via.placeholder.com/300x200.png?text=Template+1", caption="Template 1")
# st.image("https://via.placeholder.com/300x200.png?text=Template+2", caption="Template 2")

# st.button("➕ Use This Template")


# import streamlit as st
# import numpy as np
# import cv2
# from PIL import Image, ImageDraw, ImageFont
# from rembg import remove
# from io import BytesIO
# from paddleocr import PaddleOCR

# # ================= FUNCTIONS =====================

# def get_person_bbox_from_original(uploaded_file):
#     uploaded_file.seek(0)
#     result = remove(uploaded_file.read())
#     img_rgba = Image.open(BytesIO(result)).convert("RGBA")
#     alpha = np.array(img_rgba.split()[-1])
#     mask = (alpha > 0).astype(np.uint8) * 255
#     coords = cv2.findNonZero(mask)
#     x, y, w, h = cv2.boundingRect(coords)
#     return mask, (x, y, x + w, y + h)


# def replace_person_with_user_mask_fit(template_file, user_file, resize_factor=1.0):
#     # Read template and user images from uploaded files
#     template_file.seek(0)
#     user_file.seek(0)

#     original_img = Image.open(template_file).convert("RGB")
#     original_np = np.array(original_img)

#     person_mask, person_bbox = get_person_bbox_from_original(template_file)

#     image_cv = cv2.cvtColor(original_np, cv2.COLOR_RGB2BGR)
#     result_cleaned = cv2.inpaint(image_cv, person_mask, 3, cv2.INPAINT_TELEA)
#     result_cleaned_rgb = cv2.cvtColor(result_cleaned, cv2.COLOR_BGR2RGB)

#     user_cutout = remove(user_file.read())
#     user_rgba = Image.open(BytesIO(user_cutout)).convert("RGBA")

#     bbox_width = person_bbox[2] - person_bbox[0]
#     bbox_height = person_bbox[3] - person_bbox[1]
#     user_width, user_height = user_rgba.size

#     base_scale = min(bbox_width / user_width, bbox_height / user_height) * 0.95
#     final_scale = base_scale * resize_factor

#     new_width = int(user_width * final_scale)
#     new_height = int(user_height * final_scale)

#     user_resized = user_rgba.resize((new_width, new_height), Image.Resampling.LANCZOS)

#     # Calculate center point for placing
#     mask_region = person_mask[person_bbox[1]:person_bbox[3], person_bbox[0]:person_bbox[2]]
#     moments = cv2.moments(mask_region)
#     if moments["m00"] != 0:
#         cx = int(moments["m10"] / moments["m00"])
#         cy = int(moments["m01"] / moments["m00"])
#     else:
#         cx, cy = bbox_width // 2, bbox_height // 2

#     paste_x = max(0, min(person_bbox[0] + cx - new_width // 2, original_img.width - new_width))
#     paste_y = max(0, min(person_bbox[1] + cy - new_height // 2, original_img.height - new_height))

#     background_cleaned = Image.fromarray(result_cleaned_rgb).convert("RGBA")
#     final = background_cleaned.copy()
#     final.paste(user_resized, (paste_x, paste_y), user_resized)

#     return final.convert("RGB")


# def detect_and_edit_text_paddleocr(pil_image):
#     ocr = PaddleOCR(use_angle_cls=True, lang='en')
#     buffered = BytesIO()
#     pil_image.save(buffered, format="PNG")
#     img_bytes = buffered.getvalue()
#     result = ocr.ocr(img_bytes, cls=True)

#     img = pil_image.convert("RGB")
#     draw = ImageDraw.Draw(img)
#     img_cv = np.array(img)

#     fallback_font = ImageFont.load_default()

#     for line in result:
#         for box, (text, conf) in line:
#             if conf < 0.5 or text.strip() == "":
#                 continue

#             x1, y1 = map(int, box[0])
#             x2, y2 = map(int, box[2])
#             w, h = x2 - x1, y2 - y1

#             margin = 3
#             x1c = max(0, x1 - margin)
#             y1c = max(0, y1 - margin)
#             x2c = min(img.width, x2 + margin)
#             y2c = min(img.height, y2 + margin)

#             outer_box = img_cv[y1c:y2c, x1c:x2c]
#             parts = [outer_box[:margin, :], outer_box[-margin:, :], outer_box[:, :margin], outer_box[:, -margin:]]
#             bg_pixels = np.vstack([arr.reshape(-1, 3) for arr in parts if arr.size > 0])
#             avg_bg_color = tuple(np.mean(bg_pixels, axis=0).astype(int)) if bg_pixels.size > 0 else (255, 255, 255)

#             inner_box = img_cv[y1:y2, x1:x2]
#             gray_inner = cv2.cvtColor(inner_box, cv2.COLOR_RGB2GRAY)
#             _, mask = cv2.threshold(gray_inner, 180, 255, cv2.THRESH_BINARY_INV)
#             mask_bool = mask > 0
#             avg_text_color = tuple(np.mean(inner_box[mask_bool], axis=0).astype(int)) if np.any(mask_bool) else (0, 0, 0)

#             draw.rectangle([x1, y1, x2, y2], fill=avg_bg_color)

#             replacement = st.text_input(f"Replace '{text}' with:", key=f"{x1}_{y1}")
#             if replacement == "":
#                 replacement = text

#             try:
#                 font = ImageFont.truetype("arial.ttf", size=h)
#             except:
#                 font = fallback_font

#             draw.text((x1, y1), replacement, fill=avg_text_color, font=font)

#     return img


# # ================= STREAMLIT APP =====================

# st.set_page_config(page_title="Template Editor", page_icon="🎨", layout="wide")
# st.title("🎨 Template Editor with Person Replace & Text Edit")

# st.sidebar.header("🔧 Upload Files")
# template_file = st.sidebar.file_uploader("Upload Template Image", type=["png", "jpg", "jpeg"])
# user_file = st.sidebar.file_uploader("Upload Your Image", type=["png", "jpg", "jpeg"])

# resize_factor = st.sidebar.slider("Resize Person Image", 0.5, 2.0, 1.0)

# if template_file and user_file:
#     st.subheader("🖼️ Template Preview")
#     st.image(template_file, caption="Template", use_column_width=True)
#     st.image(user_file, caption="Your Image", use_column_width=True)

#     if st.button("🚀 Replace Person in Template"):
#         result_img = replace_person_with_user_mask_fit(template_file, user_file, resize_factor)
#         st.image(result_img, caption="After Person Replacement", use_column_width=True)

#         st.subheader("✍️ Text Editing")
#         edited_img = detect_and_edit_text_paddleocr(result_img)
#         st.image(edited_img, caption="Final Edited Template", use_column_width=True)

#         buffered = BytesIO()
#         edited_img.save(buffered, format="PNG")
#         st.download_button(
#             label="📥 Download Final Image",
#             data=buffered.getvalue(),
#             file_name="final_template.png",
#             mime="image/png"
#         )
# else:
#     st.info("👈 Please upload both the template image and your image to start.")


import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
from io import BytesIO
from paddleocr import PaddleOCR
import os

# ================= FUNCTIONS =====================

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
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
    else:
        cx, cy = bbox_width // 2, bbox_height // 2

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

    detected_text_boxes = []

    for line in result:
        for box, (text, conf) in line:
            if conf >= 0.5 and text.strip() != "":
                x1, y1 = map(int, box[0])
                x2, y2 = map(int, box[2])
                detected_text_boxes.append({
                    "box": (x1, y1, x2, y2),
                    "text": text
                })

    return detected_text_boxes


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
        w, h = x2 - x1, y2 - y1
        replacement = user_inputs[idx]

        # Background color estimation
        margin = 3
        x1c = max(0, x1 - margin)
        y1c = max(0, y1 - margin)
        x2c = min(img.width, x2 + margin)
        y2c = min(img.height, y2 + margin)

        outer_box = img_cv[y1c:y2c, x1c:x2c]
        parts = [outer_box[:margin, :], outer_box[-margin:, :], outer_box[:, :margin], outer_box[:, -margin:]]
        bg_pixels = np.vstack([arr.reshape(-1, 3) for arr in parts if arr.size > 0])
        avg_bg_color = tuple(np.mean(bg_pixels, axis=0).astype(int)) if bg_pixels.size > 0 else (255, 255, 255)

        # Text color estimation
        inner_box = img_cv[y1:y2, x1:x2]
        gray_inner = cv2.cvtColor(inner_box, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray_inner, 180, 255, cv2.THRESH_BINARY_INV)
        mask_bool = mask > 0
        avg_text_color = tuple(np.mean(inner_box[mask_bool], axis=0).astype(int)) if np.any(mask_bool) else (0, 0, 0)

        draw.rectangle([x1, y1, x2, y2], fill=avg_bg_color)

        try:
            font = ImageFont.truetype("arial.ttf", size=h)
        except:
            font = fallback_font

        draw.text((x1, y1), replacement, fill=avg_text_color, font=font)

    return img


# ================= STREAMLIT APP =====================

# ================= STREAMLIT APP =====================

st.set_page_config(page_title="Template Editor", page_icon="🎨", layout="wide")
st.title("🎨 Template Editor with Person Replace & Text Edit")

st.sidebar.header("🔧 Upload Files")


import os

# 🔁 Check if a template was selected from the gallery
template_file = None
if "uploaded_template_file" in st.session_state:
    template_path = st.session_state["uploaded_template_file"]
    if os.path.exists(template_path):
        with open(template_path, "rb") as f:
            template_bytes = f.read()
        template_file = BytesIO(template_bytes)
        st.sidebar.success(f"✅ Loaded template from gallery: {os.path.basename(template_path)}")
    else:
        st.sidebar.warning("⚠️ Template path not found. Please upload manually.")
        template_file = st.sidebar.file_uploader("Upload Template Image", type=["png", "jpg", "jpeg"])
else:
    template_file = st.sidebar.file_uploader("Upload Template Image", type=["png", "jpg", "jpeg"])


user_file = st.sidebar.file_uploader("Upload Your Image", type=["png", "jpg", "jpeg"], key="user_upload")

resize_factor = st.sidebar.slider("Resize Person Image", 0.5, 2.0, 1.0, key="resize_factor")

# Initialize session variables if not exist
if "replaced_img" not in st.session_state:
    st.session_state["replaced_img"] = None
if "text_boxes" not in st.session_state:
    st.session_state["text_boxes"] = None


# Run person replacement when button is clicked
if template_file and user_file:
    st.subheader("🖼️ Template Preview")
    st.image(template_file, caption="Template", use_column_width=True)
    st.image(user_file, caption="Your Image", use_column_width=True)

    if st.button("🚀 Replace Person in Template"):
        replaced_img = replace_person_with_user_mask_fit(template_file, user_file, resize_factor)
        st.session_state["replaced_img"] = replaced_img
        st.session_state["text_boxes"] = detect_text_paddleocr(replaced_img)
        st.success("✅ Person replaced successfully!")

# Show replaced image if it exists
if st.session_state["replaced_img"] is not None:
    st.subheader("✅ Person Replaced Image")
    st.image(st.session_state["replaced_img"], caption="After Person Replacement", use_column_width=True)

    st.subheader("✍️ Text Editing Section")

    text_boxes = st.session_state["text_boxes"]
    user_inputs = []

    for idx, item in enumerate(text_boxes):
        user_input = st.text_input(f"Replace '{item['text']}' with:", key=f"text_{idx}")
        if user_input.strip() == "":
            user_input = item['text']
        user_inputs.append(user_input)

    if st.button("🎨 Generate Final Image"):
        final_img = apply_text_edits(st.session_state["replaced_img"], text_boxes, user_inputs)
        st.image(final_img, caption="🎉 Final Edited Template", use_column_width=True)

        buffered = BytesIO()
        final_img.save(buffered, format="PNG")
        st.download_button(
            label="📥 Download Final Image",
            data=buffered.getvalue(),
            file_name="final_template.png",
            mime="image/png"
        )
        
    if "uploaded_template_file" in st.session_state:
        del st.session_state["uploaded_template_file"]
    
else:
    st.info("👈 Please upload both the template image and your image to start.")
