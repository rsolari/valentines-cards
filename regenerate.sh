#!/bin/bash
# Regenerate cards with old/new comparison

TEMPLATES_DIR="assets/templates"
FRONT="greek_card_front.png"
BACK="greek_card_back.png"

echo "=== Card Regeneration Script ==="

# Step 1: Rename current files to _old
echo "Step 1: Backing up current files..."
if [ -f "$TEMPLATES_DIR/$FRONT" ]; then
    mv "$TEMPLATES_DIR/$FRONT" "$TEMPLATES_DIR/${FRONT%.png}_old.png"
    echo "  Renamed $FRONT -> ${FRONT%.png}_old.png"
fi
if [ -f "$TEMPLATES_DIR/$BACK" ]; then
    mv "$TEMPLATES_DIR/$BACK" "$TEMPLATES_DIR/${BACK%.png}_old.png"
    echo "  Renamed $BACK -> ${BACK%.png}_old.png"
fi

# Step 2: Generate new files
echo "Step 2: Generating new cards..."
python src/greek_design_system.py

# Step 3: Compare file sizes
echo ""
echo "Step 3: Comparing files..."
if [ -f "$TEMPLATES_DIR/${FRONT%.png}_old.png" ] && [ -f "$TEMPLATES_DIR/$FRONT" ]; then
    OLD_SIZE=$(stat -c%s "$TEMPLATES_DIR/${FRONT%.png}_old.png")
    NEW_SIZE=$(stat -c%s "$TEMPLATES_DIR/$FRONT")
    echo "  Front card: OLD=${OLD_SIZE} bytes, NEW=${NEW_SIZE} bytes"
    if [ "$OLD_SIZE" -eq "$NEW_SIZE" ]; then
        echo "  WARNING: Front card sizes are identical!"
    else
        echo "  OK: Front card size changed by $((NEW_SIZE - OLD_SIZE)) bytes"
    fi
fi

if [ -f "$TEMPLATES_DIR/${BACK%.png}_old.png" ] && [ -f "$TEMPLATES_DIR/$BACK" ]; then
    OLD_SIZE=$(stat -c%s "$TEMPLATES_DIR/${BACK%.png}_old.png")
    NEW_SIZE=$(stat -c%s "$TEMPLATES_DIR/$BACK")
    echo "  Back card: OLD=${OLD_SIZE} bytes, NEW=${NEW_SIZE} bytes"
    if [ "$OLD_SIZE" -eq "$NEW_SIZE" ]; then
        echo "  WARNING: Back card sizes are identical!"
    else
        echo "  OK: Back card size changed by $((NEW_SIZE - OLD_SIZE)) bytes"
    fi
fi

# Step 4: Stage and commit
echo ""
echo "Step 4: Staging and committing..."
git add -A
git status --short

echo ""
read -p "Commit message: " COMMIT_MSG
git commit -m "$COMMIT_MSG"

# Step 5: Push
echo ""
echo "Step 5: Pushing..."
git push -u origin claude/valentine-card-design-nE42M

echo ""
echo "=== Done ==="
echo "Old files preserved as *_old.png for comparison"
