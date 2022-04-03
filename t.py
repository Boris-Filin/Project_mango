import re
def handle_tags(line):
	tags_text = re.search(r"\{.*\}", line)
	if tags_text == None:
		return None

	tags = {}
	tags_strings = re.sub("\{|\}", "", tags_text.group(0)).split(",")
	for tag_string in tags_strings:
		tag = tag_string.strip()
		if not ":" in tag:
			continue
		key = tag[:tag.find(":")]
		val = tag[tag.find(":") + 1:]
		tags[key] = val

	return tags

print(handle_tags("s 1 1 0 0 {slab:True, fill:#}"))