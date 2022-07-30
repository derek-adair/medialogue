while true; do
ag -l | entr -dc pytest --pdb $@
done
