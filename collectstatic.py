import hashlib
import os
import shutil

DATA_DIR = "data"

COLOR_RESET = "\033[0m"
COLOR_OK = "\033[92m"
COLOR_STATUS = "\033[94m"
COLOR_DIM = "\033[90m"


ALLOWED_EXTENSIONS = set([
	".png", ".jpg", ".bmp", ".tga",
	".pcx", ".ppm", ".psd", ".wal", ".rgb",
	".ogg", ".x", ".b3d", ".md2", ".obj"
])


def sha1(filename):
	f = open(filename, "rb")
	h = hashlib.sha1(f.read()).hexdigest()
	f.close()
	return h


def copy_static(path):
	new_path = sha1(path)
	new_dirs = os.path.join(DATA_DIR, new_path[0], new_path[1], new_path[2], new_path[3])
	os.makedirs(new_dirs, exist_ok=True)
	shutil.copyfile(path, os.path.join(new_dirs, new_path))


def collect_static(path):
	print(COLOR_OK + "Collecting static from {}".format(path) + COLOR_RESET)
	count = 0
	for name in os.listdir(path):
		file_path = os.path.join(path, name)
		if os.path.isfile(file_path) and os.path.splitext(file_path)[1] in ALLOWED_EXTENSIONS:
			copy_static(file_path)
			count += 1
	if count:
		print(COLOR_STATUS + "copied {} file{}".format(count, "" if count == 1 else "s") + COLOR_RESET)


def collect_mod(path):
	print(COLOR_DIM + "Entering {}".format(path) + COLOR_RESET)
	if os.path.exists(os.path.join(path, "modpack.txt")):
		collect_mods(path)
		return
	for media_dir in ["textures", "sounds", "media", "models"]:
		media_path = os.path.join(path, media_dir)
		if os.path.exists(media_path) and os.path.isdir(media_path):
			collect_static(media_path)


def collect_mods(path):
	print(COLOR_DIM + "Collecting mods in {}".format(path) + COLOR_RESET)
	for mod in os.listdir(path):
		mod_path = os.path.join(path, mod)
		if os.path.isdir(mod_path) and not mod.startswith("."):
			collect_mod(mod_path)


def main():
	collect_mods("mods")


if __name__ == "__main__":
	main()
