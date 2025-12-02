#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime
from pathlib import Path

def get_nested_value(data, path):
    """获取嵌套字典中的值，支持点分隔路径"""
    keys = path.split('.')
    current = data
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return None

def extract_fields_from_locales(locales_dir):
    """从语言文件中提取所有字段"""
    locales = {}
    for lang in ['zh', 'en', 'ar']:
        file_path = os.path.join(locales_dir, f"{lang}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                locales[lang] = json.load(f)
    return locales

def extract_fields_from_content_mapping(content_dir):
    """从内容映射文件中提取字段信息"""
    content_mappings = {}
    mapping_files = [
        'content-mapping-SpeakUp.json',
        'content-mapping-GradeUp.json',
        'content-mapping-ScoreBoost.json'
    ]

    for file in mapping_files:
        file_path = os.path.join(content_dir, file)
        if os.path.exists(file_path):
            page_name = file.replace('content-mapping-', '').replace('.json', '')
            with open(file_path, 'r', encoding='utf-8') as f:
                content_mappings[page_name] = json.load(f)

    return content_mappings

def scan_html_files(public_dir):
    """扫描HTML文件中的data-i18n属性"""
    html_files = ['SpeakUp.html', 'GradeUp.html', 'ScoreBoost.html', 'i18n-test-suite.html', 'page-template.html']
    i18n_fields = {}

    for html_file in html_files:
        file_path = os.path.join(public_dir, html_file)
        if os.path.exists(file_path):
            page_name = html_file.replace('.html', '')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 查找所有data-i18n属性
            pattern = r'data-i18n="([^"]+)"'
            matches = re.finditer(pattern, content)

            for match in matches:
                field_key = match.group(1)
                # 获取前后文来构建CSS选择器
                start_pos = max(0, match.start() - 200)
                end_pos = min(len(content), match.end() + 200)
                context = content[start_pos:end_pos]

                # 尝试构建CSS选择器
                selector_pattern = r'([^<>\s]*)\s+[^>]*data-i18n="[^"]*"'
                selector_match = re.search(selector_pattern, context)
                selector = f'[data-i18n="{field_key}"]'  # 默认选择器

                if field_key not in i18n_fields:
                    i18n_fields[field_key] = {}
                i18n_fields[field_key][page_name] = {
                    'selector': selector,
                    'found_in_html': True
                }

    return i18n_fields

def determine_section_id(field_key):
    """根据字段键确定section ID"""
    parts = field_key.split('.')
    if len(parts) >= 2:
        return parts[0]  # 第一部分通常是section
    return 'unknown'

def assess_safety(field_key, element_type):
    """评估替换的安全性"""
    # 关键字段，修改风险较高
    high_risk_fields = [
        'meta.title',  # SEO标题
        'hero.title',  # 主标题
        'cta.button'   # 按钮文本
    ]

    if field_key in high_risk_fields:
        return False, "关键字段，修改可能影响SEO或用户体验"

    # 一般描述性文本相对安全
    if 'desc' in field_key or 'subtitle' in field_key:
        return True, "描述性文本，相对安全"

    # 特征列表文本
    if 'feature' in field_key:
        return True, "特征列表项，相对安全"

    return True, "一般文本字段"

def suggest_max_length(field_key):
    """根据字段类型建议最大长度"""
    if 'title' in field_key:
        return 60
    elif 'subtitle' in field_key:
        return 120
    elif 'desc' in field_key:
        return 200
    elif 'tag' in field_key:
        return 30
    elif 'button' in field_key or 'cta' in field_key:
        return 25
    else:
        return 100

def collect_all_field_paths(data, prefix=''):
    """递归收集所有字段路径，但只包括叶子节点（非对象）"""
    field_paths = []

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{prefix}.{key}" if prefix else key

            # 如果值是字典，继续递归，但不把当前路径作为字段
            if isinstance(value, dict):
                field_paths.extend(collect_all_field_paths(value, current_path))
            # 如果值不是字典（字符串、数字等），这是我们要的字段
            else:
                field_paths.append(current_path)

    return field_paths

def generate_text_fields(locales, content_mappings, i18n_fields):
    """生成文本字段清单"""
    text_fields = []
    all_field_keys = set()

    # 从语言文件中收集所有叶子节点字段键
    for lang_data in locales.values():
        field_paths = collect_all_field_paths(lang_data)
        all_field_keys.update(field_paths)

    # 为每个字段生成清单项
    for field_key in sorted(all_field_keys):
        section_id = determine_section_id(field_key)

        # 获取三语内容
        current_text = {}
        for lang in ['zh', 'en', 'ar']:
            value = get_nested_value(locales.get(lang, {}), field_key)
            current_text[lang] = value if value is not None else ""

        # 确定来源
        source = "locales"

        # 确定页面ID
        page_id = "SpeakUp"  # 默认
        if field_key in i18n_fields:
            pages = list(i18n_fields[field_key].keys())
            if pages:
                page_id = pages[0]  # 取第一个找到的页面

        # 获取CSS选择器
        selector = f'[data-i18n="{field_key}"]'
        if field_key in i18n_fields and page_id in i18n_fields[field_key]:
            selector = i18n_fields[field_key][page_id].get('selector', selector)

        # 评估安全性
        safe_to_replace, risk_note = assess_safety(field_key, 'text')

        # 建议最大长度
        max_length_suggest = suggest_max_length(field_key)

        text_field = {
            "fieldKey": field_key,
            "pageId": page_id,
            "sectionId": section_id,
            "selector": selector,
            "currentText": current_text,
            "source": source,
            "safeToReplace": safe_to_replace,
            "riskNote": risk_note,
            "maxLengthSuggest": max_length_suggest
        }

        text_fields.append(text_field)

    return text_fields

def scan_image_assets(project_root):
    """扫描图片资源和emoji图标"""
    image_fields = []

    # 查找所有图片文件
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']
    image_files = []

    for root, dirs, files in os.walk(project_root):
        # 跳过 .git 目录
        if '.git' in root:
            continue

        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(root, file))

    # 检查HTML中的图片引用和emoji
    html_files = ['SpeakUp.html', 'GradeUp.html', 'ScoreBoost.html', 'i18n-test-suite.html', 'page-template.html']

    # emoji映射表，为不同用途提供建议
    emoji_meanings = {
        '🎯': {'purpose': 'target/goal', 'suggest_alt': 'target-icon.png'},
        '🌍': {'purpose': 'global/world', 'suggest_alt': 'global-icon.png'},
        '📈': {'purpose': 'growth/chart', 'suggest_alt': 'growth-chart.png'},
        '👩‍🏫': {'purpose': 'female teacher', 'suggest_alt': 'teacher-female.png'},
        '👨‍🏫': {'purpose': 'male teacher', 'suggest_alt': 'teacher-male.png'},
        '👨‍👩‍👧‍👦': {'purpose': 'family', 'suggest_alt': 'family-icon.png'},
        '📚': {'purpose': 'books/education', 'suggest_alt': 'books-icon.png'},
        '🏆': {'purpose': 'achievement/trophy', 'suggest_alt': 'trophy-icon.png'},
        '🌟': {'purpose': 'star/feature', 'suggest_alt': 'star-icon.png'},
        '⭐': {'purpose': 'star/rating', 'suggest_alt': 'rating-star.png'}
    }

    for html_file in html_files:
        file_path = os.path.join(project_root, 'public', html_file)
        if os.path.exists(file_path):
            page_id = html_file.replace('.html', '')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 查找img标签
            img_pattern = r'<img[^>]*src="([^"]*)"[^>]*>'
            img_matches = re.finditer(img_pattern, content, re.IGNORECASE)

            img_index = 0
            for match in img_matches:
                img_tag = match.group(0)
                src_path = match.group(1)

                # 跳过外部URL
                if src_path.startswith('http'):
                    continue

                asset_id = f"{page_id}_img_{img_index}"
                selector = f'{page_id} img:nth-of-type({img_index + 1})'

                # 尝试获取更多属性
                class_match = re.search(r'class="([^"]*)"', img_tag)
                css_class = class_match.group(1) if class_match else ""

                # 如果有class，使用更精确的选择器
                if css_class:
                    selector = f'{page_id} .{css_class.replace(" ", ".")}'

                image_field = {
                    "assetId": asset_id,
                    "pageId": page_id,
                    "selector": selector,
                    "currentPath": src_path if src_path else None,
                    "currentSize": "unknown",
                    "ratioLock": True,
                    "safeToReplace": True,
                    "riskNote": "HTML中的图片引用",
                    "suggestFormat": "png"
                }

                image_fields.append(image_field)
                img_index += 1

            # 查找emoji图标
            emoji_pattern = r'([🎯🌍📈👩‍🏫👨‍🏫👨‍👩‍👧‍👦📚🏆🌟⭐])'
            emoji_matches = re.finditer(emoji_pattern, content)

            emoji_counts = {}
            emoji_positions = {}

            for match in emoji_matches:
                emoji = match.group(1)
                position = match.start()

                if emoji not in emoji_counts:
                    emoji_counts[emoji] = 0
                    emoji_positions[emoji] = []

                emoji_counts[emoji] += 1
                emoji_positions[emoji].append(position)

            # 为每个emoji创建资源记录
            for emoji, count in emoji_counts.items():
                emoji_info = emoji_meanings.get(emoji, {
                    'purpose': 'unknown',
                    'suggest_alt': 'icon-replacement.png'
                })

                # 获取emoji的上下文来构建选择器
                first_pos = emoji_positions[emoji][0]
                start_pos = max(0, first_pos - 100)
                end_pos = min(len(content), first_pos + 100)
                context = content[start_pos:end_pos]

                # 尝试找到周围的class或id
                class_match = re.search(r'class="([^"]*)"[^<]*.{0,50}' + re.escape(emoji), context)
                div_match = re.search(r'<div[^>]*>(.{0,50}' + re.escape(emoji) + ')', context)

                selector = f'{page_id} .emoji-{emoji.replace("🏫", "teacher").replace("🎯", "target").replace("🌍", "global").replace("📈", "growth").replace("👨‍👩‍👧‍👦", "family").replace("📚", "books").replace("🏆", "trophy").replace("🌟", "star-feature").replace("⭐", "star-rating")}'

                if class_match:
                    css_class = class_match.group(1)
                    selector = f'{page_id} .{css_class.split()[0]}'
                elif div_match:
                    selector = f'{page_id} div:contains("{emoji}")'

                image_field = {
                    "assetId": f"{page_id}_{emoji_info['purpose'].replace('/', '_')}",
                    "pageId": page_id,
                    "selector": selector,
                    "currentPath": None,
                    "currentSize": "emoji",
                    "ratioLock": True,
                    "safeToReplace": True,
                    "riskNote": f"Emoji图标 '{emoji}' - 出现{count}次，建议替换为{emoji_info['suggest_alt']}",
                    "suggestFormat": "png",
                    "emoji": emoji,
                    "count": count,
                    "purpose": emoji_info['purpose'],
                    "suggestReplacement": emoji_info['suggest_alt']
                }

                image_fields.append(image_field)

    # 添加本地图片文件
    for img_file in image_files:
        rel_path = os.path.relpath(img_file, project_root)
        filename = os.path.basename(img_file)

        # 简单的尺寸检测（这里只是占位符）
        size_info = "unknown"

        image_field = {
            "assetId": filename.replace('.', '_'),
            "pageId": "assets",
            "selector": filename,
            "currentPath": rel_path,
            "currentSize": size_info,
            "ratioLock": True,
            "safeToReplace": True,
            "riskNote": "静态资源文件",
            "suggestFormat": os.path.splitext(filename)[1][1:].lower()
        }

        image_fields.append(image_field)

    return image_fields

def main():
    """主函数"""
    project_root = "/Users/jin/landing-pages-deploy"
    assets_dir = os.path.join(project_root, "assets")
    locales_dir = os.path.join(assets_dir, "locales")
    content_dir = os.path.join(assets_dir, "content")
    public_dir = os.path.join(project_root, "public")

    print("正在分析语言文件...")
    locales = extract_fields_from_locales(locales_dir)

    print("正在扫描HTML文件...")
    i18n_fields = scan_html_files(public_dir)

    print("正在生成文本字段清单...")
    text_fields = generate_text_fields(locales, {}, i18n_fields)

    print("正在扫描图片资源...")
    image_fields = scan_image_assets(project_root)

    # 生成最终JSON
    checklist = {
        "meta": {
            "generatedAt": datetime.now().isoformat(),
            "projectRoot": project_root,
            "pagesScanned": ["SpeakUp", "GradeUp", "ScoreBoost", "i18n-test-suite", "page-template"],
            "totalTextFields": len(text_fields),
            "totalImageFields": len(image_fields)
        },
        "textFields": text_fields,
        "imageFields": image_fields
    }

    # 输出文件
    output_path = os.path.join(assets_dir, "arabic-replace-checklist.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(checklist, f, ensure_ascii=False, indent=2)

    print(f"\n生成完成！")
    print(f"输出文件: {output_path}")
    print(f"文本字段总数: {len(text_fields)}")
    print(f"图片字段总数: {len(image_fields)}")

    # 显示一些统计信息
    print(f"\n=== 文本字段统计 ===")
    section_count = {}
    for field in text_fields:
        section = field['sectionId']
        section_count[section] = section_count.get(section, 0) + 1

    for section, count in sorted(section_count.items()):
        print(f"{section}: {count} 个字段")

if __name__ == "__main__":
    main()