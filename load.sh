cp settings/training/tiny.txt env.list
echo 'DATABASE=${DATABASE}' >> env.list
ENTRYPOINT=training.sh bash start.sh