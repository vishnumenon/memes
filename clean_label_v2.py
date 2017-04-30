# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.f

from __future__ import unicode_literals
import json
import io
import os
import re
import sys

# Hold the meme lists
commentCategories = {
    'nessie': [],
    'switcharoo': [],
    'rickroll': [],
    'aesthetic': [],
    'emoji': [],
    'wot': [],
    'ratings': [],
    'obama': []
}

offset = 0

def categorize_comment(comment):
    # For each comment, check it with the Regular Expressions for our 8 pre-selected memes
    # If it matches one of them, then add it to that meme's list
    # if not, discard
    if re.search(r"(tree fitty|tree fiddy|nessie|loch ness monster|the paleolithic era)+", comment["body"], re.I) is not None:
        commentCategories["nessie"].append(comment)
    if re.search(r"(ahh|ol|reddit).{1,20}oo\]|hold my [A-Za-z]+, I[']{0,1}m goin[g']{0,1} in", comment["body"], re.I) is not None:
        commentCategories["switcharoo"].append(comment)
    if re.search(r"watch\?v\=(dQw4w9WgXcQ|6_b7RDuLwcI|dGeEuyG_DIc|IO9XlQrEt2Y)", comment["body"]) is not None:
        commentCategories['rickroll'].append(comment)
    if re.search(r"([A-Za-z]{1} ){5,}", comment["body"]) is not None:
        commentCategories["aesthetic"].append(comment)
    for emoji in ["( ͡° ͜ʖ ͡°)", "¯\_(ツ)_/¯", "(ﾉ◕ヮ◕)ﾉ", "(ง ͠° ͟ل͜ ͡°)ง", "(ง'̀-'́)ง", "(◕‿◕✿)", "┬──┬", "┬─┬", "/╲/\╭( ͡° ͡° ͜ʖ ͡° ͡°)╮/\╱\\", "◉_◉", "\ (•◡•) /"]:
        if emoji in comment["body"]:
            commentCategories["emoji"].append(comment)
            break
    if re.search(r"wot m8|u wot|fookin|cheeky .*cun|on me mum", comment["body"], re.I) is not None:
        commentCategories["wot"].append(comment)
    if re.search(r"perfect 5\/7|r8.*8\/8|\/10 (w|with).{0,3}rice", comment["body"]) is not None:
        commentCategories["ratings"].append(comment)
    if re.search(r"thanks[,]* obama", comment["body"], re.I) is not None:
        commentCategories["obama"].append(comment)

def wrapUp():
    # Print out current offset, for resuming later
    print("Stopping at offset " + str(offset))
    filename = sys.argv[1]
    # Write output, one file per meme category
    for key in commentCategories:
        with io.open(key + "-" + filename + ".json", 'w', encoding='utf-8') as output:
            for c in commentCategories[key]:
                # Allow for Unicode in output
                output.write(json.dumps(c, ensure_ascii=False)+"\n")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

def main():
    # Allow for multiple input files, separated by commas
    f = sys.argv[1]
    # Increase buffer for faster processing
    bufsize = 65536
    # Include ability to skip to a certain offset, for processing long files in multiple intervals
    offset = long(sys.argv[2])
    commentCount = 0
    with open(f) as inputFile:
        # Skip to starting position
        inputFile.seek(offset)
        while True:
            # Read lines into the buffer
            lines = inputFile.readlines(bufsize)
            offset += bufsize
            # End when file is over
            if not lines:
                break
            for line in lines:
                # Load json comment and discard useless keys
                comment = json.loads(line)
                comment = {k: comment[k] for k in ['body', 'score', 'gilded', 'controversiality', 'subreddit', 'created_utc']}
                # Process comment by placing it in its correct category
                categorize_comment(comment)
                commentCount += 1
                if commentCount % 1000 == 0:
                    # Print out status updates
                    print("Processed " + str(commentCount) + " comments")
    wrapUp()

# Handle Ctrl-C gracefully
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
        wrapUp()
