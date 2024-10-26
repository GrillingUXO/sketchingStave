from PIL import Image
import xml.etree.ElementTree as ET
import easygui

def process_image(image_path, target_width=160, target_height=160):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((target_width, target_height)) 
    pixels = list(image.getdata())
    processed_image = Image.new('RGB', (target_width, target_height))
    processed_image.putdata(pixels)
    return [pixels[i * target_width:(i + 1) * target_width] for i in range(target_height)], processed_image

def create_musicxml_template(total_measures=400):
    score = ET.Element('score-partwise', version="3.1")

    part_list = ET.SubElement(score, 'part-list')
    score_part = ET.SubElement(part_list, 'score-part', id="P1")
    part_name = ET.SubElement(score_part, 'part-name')
    part_name.text = "Generated Part"

    part = ET.SubElement(score, 'part', id="P1")

    # 页面布局
    defaults = ET.SubElement(score, 'defaults')
    page_layout = ET.SubElement(defaults, 'page-layout')
    ET.SubElement(page_layout, 'page-height').text = "2000"
    ET.SubElement(page_layout, 'page-width').text = "1200"

    margins = ET.SubElement(page_layout, 'page-margins', type="both")
    ET.SubElement(margins, 'left-margin').text = "10"
    ET.SubElement(margins, 'right-margin').text = "10"
    ET.SubElement(margins, 'top-margin').text = "10"
    ET.SubElement(margins, 'bottom-margin').text = "10"

    system_layout = ET.SubElement(defaults, 'system-layout')
    ET.SubElement(system_layout, 'system-distance').text = "0"
    ET.SubElement(system_layout, 'staff-distance').text = "0"

    staff_layout = ET.SubElement(system_layout, 'staff-layout')
    ET.SubElement(staff_layout, 'staff-lines').text = "0"
    ET.SubElement(staff_layout, 'staff-line-color').text = "#ffffff"

    for measure_number in range(1, total_measures + 1):
        measure = ET.SubElement(part, 'measure', number=str(measure_number))

        attributes = ET.SubElement(measure, 'attributes')
        measure_width = ET.SubElement(attributes, 'measure-width')
        measure_width.text = "64"

        # 在第一个小节添加乐谱属性
        if measure_number == 1:
            divisions = ET.SubElement(attributes, 'divisions')
            divisions.text = "64"

            key = ET.SubElement(attributes, 'key')
            ET.SubElement(key, 'fifths').text = "0"  # C大调

            time = ET.SubElement(attributes, 'time')
            ET.SubElement(time, 'beats').text = "4"
            ET.SubElement(time, 'beat-type').text = "4"  # 4/4拍
            clef = ET.SubElement(attributes, 'clef')
            ET.SubElement(clef, 'sign').text = "none"  # 隐藏谱号

        # 每1o小节换行
        if measure_number % 10 == 0:
            print_attrs = ET.SubElement(measure, 'print')
            print_attrs.set('new-system', 'yes')
            system_layout = ET.SubElement(print_attrs, 'system-layout')
            margins = ET.SubElement(system_layout, 'system-margins')
            ET.SubElement(margins, 'left-margin').text = "10.0"  # 左边距
            ET.SubElement(margins, 'right-margin').text = "10.0"  # 右边距
            ET.SubElement(system_layout, 'system-distance').text = "0"

    return score

def rgb_to_hex(rgb):
    """将RGB颜色转换为十六进制字符串。"""
    return "#{:02x}{:02x}{:02x}".format(*rgb)

import xml.etree.ElementTree as ET

def add_blank_measures(score, count=9):
    part = score.find('part')
    for _ in range(count):
        measure = ET.SubElement(part, 'measure')
        
        for chord_index in range(16):
            for _ in range(20):  # 20 notes in each chord
                note = ET.SubElement(measure, 'note')
                
                pitch = ET.SubElement(note, 'pitch')
                ET.SubElement(pitch, 'step').text = 'C'
                ET.SubElement(pitch, 'octave').text = '4'
                ET.SubElement(note, 'duration').text = "1"
                ET.SubElement(note, 'type').text = "64th"
                ET.SubElement(note, 'voice').text = "1"
                ET.SubElement(note, 'stem').text = "up"
                
                notehead = ET.SubElement(note, 'notehead')
                notehead.set('color', "#FFFFFF")
                notehead.text = "normal"

def map_pixels_to_notes(score, color_image):
    part = score.find('part')
    measures = part.findall('measure')
    
    # 区块分配
    if len(color_image) != 160 or any(len(row) != 160 for row in color_image):
        raise ValueError("错误：没有正确处理图片至160*160。")
    if len(measures) < 89:
        raise ValueError("错误：没有正确映射为89个小节。")
    
    # 和弦内音符映射，E7到B1
    note_positions = [
        ('E', 7), ('C', 7), ('A', 6), ('F', 6), ('D', 6),
        ('B', 5), ('G', 5), ('E', 5), ('C', 5), ('A', 4),
        ('F', 4), ('D', 4), ('B', 3), ('G', 3), ('E', 3),
        ('C', 3), ('A', 2), ('F', 2), ('D', 2), ('B', 1)
    ]
    
    # 图像区块-小节映射
    for measure_col in range(10):
        for measure_row in range(8):
            measure_index = (measure_row * 10 + measure_col) + 9
            if measure_index >= len(measures):
                break  # Avoid index errors if XML is shorter than expected
            
            measure = measures[measure_index]
            
            # 一个小节
            x_start = measure_col * 16
            y_start = measure_row * 20
            
            # 映射
            for chord_index in range(16):
                # Each chord holds 20 notes from the 20-pixel column segment
                for note_offset, (step, octave) in enumerate(note_positions):
                    # Find the pixel in the corresponding section of the image
                    pixel_x = x_start + chord_index
                    pixel_y = y_start + note_offset
                    pixel_color = color_image[pixel_y][pixel_x]

                    hex_color = "#{:02x}{:02x}{:02x}".format(*pixel_color)
                    
                    # 音符入口
                    note = ET.SubElement(measure, 'note')
                    pitch = ET.SubElement(note, 'pitch')
                    ET.SubElement(pitch, 'step').text = step
                    ET.SubElement(pitch, 'octave').text = str(octave)
                    ET.SubElement(note, 'duration').text = "1"
                    ET.SubElement(note, 'type').text = "64th"
                    ET.SubElement(note, 'voice').text = "1"
                    ET.SubElement(note, 'stem').text = "up"
                    
                    # 符头颜色
                    notehead = ET.SubElement(note, 'notehead')
                    notehead.set('color', hex_color)
                    notehead.text = "normal"
                    
                    if note_offset > 0:
                        ET.SubElement(note, 'chord')

def generate_musicxml_with_blanks(score, color_image):
    """Generates a MusicXML with blank measures and image mapping."""
    add_blank_measures(score, 9)
    map_pixels_to_notes(score, color_image)


def save_musicxml(score, output_path="output_image.musicxml"):
    """保存MusicXML文件。"""
    tree = ET.ElementTree(score)
    tree.write(output_path, encoding="UTF-8", xml_declaration=True)
    print(f"MusicXML文件已保存至: {output_path}")

def save_processed_image(image, output_path="processed_image.png"):
    """保存处理后的图像。"""
    image.save(output_path)
    print(f"处理后的图像已保存至: {output_path}")

def generate_musicxml_from_image(image_path, output_musicxml="output_image.musicxml", output_image="processed_image.png"):
    """从图像生成相应的MusicXML文件，并保存处理后的图像。"""
    
    color_image, processed_image = process_image(image_path)

    score = create_musicxml_template()

    map_pixels_to_notes(score, color_image)

    save_musicxml(score, output_musicxml)

    save_processed_image(processed_image, output_image)

if __name__ == "__main__":
    # 使用 easygui 选择文件和保存路径
    image_path = easygui.fileopenbox(title="选择输入图像", filetypes=["*.png", "*.jpg", "*.jpeg", "*.bmp"])
    if image_path:
        output_musicxml = easygui.filesavebox(title="保存MusicXML文件", default="output_image.musicxml", filetypes=["*.musicxml"])
        output_image = easygui.filesavebox(title="保存处理后的图像", default="processed_image.png", filetypes=["*.png"])
        if output_musicxml and output_image:
            generate_musicxml_from_image(image_path, output_musicxml, output_image)
        else:
            print("未指定输出文件路径，程序终止。")
    else:
        print("未选择图像文件，程序终止。")    
