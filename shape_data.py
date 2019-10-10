import os
import re
import shutil
import csv
import utils

NO_CLUE = ( -1 , None )

def marks_prologue( line ):
    return re.search( r"^\s*prologue", line, re.IGNORECASE ) != None

def marks_proem( line ):
    return re.search( r"^\s*proem", line, re.IGNORECASE ) != None

def marks_preamble( line ):
    return re.search( r"^\s*preamble", line, re.IGNORECASE ) != None

def marks_book_one( line ):
    return re.search( r"^\s*book\s+([i1]\b|one)", line, re.IGNORECASE ) != None

def marks_part_one( line ):
    return re.search( r"^\s*part\s+[i1]\b", line, re.IGNORECASE ) != None

def marks_first_part( line ):
    return re.search( r"^\s*first\s+part", line, re.IGNORECASE ) != None

def marks_first_chapter( line ):
    # ^\s*chapter\s+[i1o]
    return re.search( r"^\s*chapter\s+([1i]|one)\b", line, re.IGNORECASE ) != None

def marks_first_chapter_number( line ):
    return re.search( r"^\s*[i1]$", line, re.IGNORECASE ) != None

def marks_first_scene( line ):
    return re.search( r"^\s*scene\s+([i1]|one)\b", line, re.IGNORECASE ) != None

def marks_contents( line ):
    return re.search( r"\s*(contents|chapters)\s*$", line, re.IGNORECASE ) != None

def marks_by( line ):
    return re.search( r"^\s*by\s*.{,30}$", line, re.IGNORECASE ) != None

def marks_the_end( line ):
    return re.search( r"^\s*the end\.?\s*$", line, re.IGNORECASE ) != None

def marks_gutenberg_end( line ):
    return re.search( r"end.*project gutenberg", line, re.IGNORECASE ) != None

def post_contents( clue, text_lines ):
    idx = clue[0] + 1
    qualifying_lines = 0
    while qualifying_lines < 3 and idx < len( text_lines ):
        line = text_lines[idx]
        qualifying_lines += 1
        if not line.strip():
            qualifying_lines = 0
        else:
            if ( sum( 1 for c in line if c.isupper() ) / len( line ) ) > 0.2:
                qualifying_lines = 0
            if ( re.search( r"\.{4,}", line ) ):  # fill periods
                qualifying_lines = 0
            if ( re.search( r"^\s*\d+", line ) ):
                qualifying_lines = 0
        idx += 1
    if qualifying_lines == 3:
        return ( idx - 3, marks_contents )
    else:
        return NO_CLUE

def post_by( clue, text_lines ):
    idx = next( idx for idx, line in enumerate( text_lines[clue[0]:] ) if len( line ) > 60 )
    return ( clue[0] + idx, clue[1] )

def find_from_bottom( text_lines, matcher ):
    for idx, line in enumerate( reversed( text_lines ) ):
        if matcher( line ):
            return len( text_lines ) - idx
    return -1

def find_most_inner_clue( clues, matchers ):
    return next( ( clue for clue in clues if( clue[1] in matchers ) ), NO_CLUE )

def collect_and_analyse_clues( path, file_name ):
    with open( os.path.join( path, file_name ), "r" ) as txt_file:
        print( "Processing: {}".format( file_name ) )
        text = txt_file.read().split( "\n" )
    if ( len( text ) > 1000 ):
        text = text[0:999]
    # We only need to know what lowest level match takes plase on a line
    # In case od e.g. "Book 1, Chapter 1" it is enough to match on "Chapter 1"
    # thus there is no need to run all matchers on each line, just
    # run them on the text to identify what lines they match.
    clues = []
    matchers_by_presedence = [ marks_prologue, marks_proem, marks_preamble, marks_book_one, marks_part_one, marks_first_part, marks_first_chapter, marks_first_chapter_number, marks_first_scene, marks_contents, marks_by ]
    for matcher in matchers_by_presedence:
        idx = find_from_bottom( text, matcher )
        if not idx == -1:
            clues.append( ( idx, matcher ) )
    # Now in principle we want to return the first chapter heading found from the
    # bottom up, unless a book or part heading is very near above it, then that
    # unless a prologue or proem is just above it
    # so it's clue for clue unless next clue take precedence and is near
    if len( clues ) > 0:
        clues.reverse();
        best_clue = find_most_inner_clue( clues, [ marks_prologue, marks_proem, marks_preamble ] )
        if best_clue == NO_CLUE:
            best_clue = find_most_inner_clue( clues, [ marks_book_one ] )
            # However, it happens that there will be "Book I" in a
            # "CONTENTS" but then not a "Book I" right before the
            # "Chapter 1" start…
            inner_most_chapter_clue = find_most_inner_clue( clues, [ marks_first_chapter, marks_first_chapter_number ] )
            if best_clue[0] < ( inner_most_chapter_clue[0] - 10 ):
                best_clue = NO_CLUE
        if best_clue == NO_CLUE:
            best_clue = find_most_inner_clue( clues, [ marks_part_one, marks_first_part ] )
        if best_clue == NO_CLUE:
            best_clue = find_most_inner_clue( clues, [ marks_first_chapter, marks_first_chapter_number ] )
        if best_clue == NO_CLUE:
            best_clue = find_most_inner_clue( clues, [ marks_first_scene ] )
        if best_clue == NO_CLUE:
            best_clue = find_most_inner_clue( clues, [ marks_contents ] )
            if best_clue != NO_CLUE:
                best_clue = post_contents( best_clue, text )
        if best_clue == NO_CLUE:
            best_clue = find_most_inner_clue( clues, [ marks_by ] )
            if best_clue != NO_CLUE:
                best_clue = post_by( best_clue, text )
        return ( best_clue )
    else:
        return NO_CLUE

def match_story_clues( path, file_name, matchers ):
    with open( os.path.join( path, file_name ), "r" ) as text:
        line = text.readline()
        idx = 1
        while line:
            for matcher in matchers:
                if matcher( line ):
                    return ( idx, matcher )
            line = text.readline()
            idx += 1
    return (idx, None )

def match_story_start_clues( path, file_name ):
    matchers = [ marks_prologue, marks_proem, marks_book_one, marks_part_one, marks_first_part, marks_first_chapter, marks_first_chapter_number ]
    return match_story_clues( path, file_name, matchers )

def match_story_end_clues( path, file_name ):
    matchers = [ marks_the_end, marks_gutenberg_end ]
    return match_story_clues( path, file_name, matchers )

def match_towards_top( path, file_name ):
    with open( os.path.join( path, file_name ), "r" ) as txt_file:
        text = txt_file.read()
    text = text.split( "\n" )
    idx = 1000
    text = text[0:idx]
    text.reverse()
    matchers = [ marks_prologue, marks_proem, marks_book_one, marks_part_one, marks_first_part, marks_first_chapter, marks_first_chapter_number ]
    # matchers.reverse()
    for line in text:
        mn = 0
        for matcher in matchers:
            if matcher( line ):
                return ( idx, "{}:{}".format( matcher.__name__, mn) )
                line = text.readline()
            mn += 1
        idx -= 1
    return NO_CLUE

def moving_average( numbers, N ):
    cumsum, moving_aves = [0], []
    for i, x in enumerate(numbers, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            #can do stuff with moving_ave here
            moving_aves.append(moving_ave)
    return moving_aves

def line_lenght_histo( path, file_name ):
    lengths = []
    with open( os.path.join( path, file_name ), "r" ) as text:
        for i in range(500):
            line = text.readline()
            lengths.append( len( line ) )
    running_means = moving_average( lengths, 20 )
    overall_mean = sum( lengths )/len(lengths)
    idx = next( i for i, v in enumerate( running_means ) if v > overall_mean )
    return idx

def find_story_start( path, strategy ):
    txts = utils.get_file_names_by_extension( path, "txt" )
    txt_starts = {}
    for txt in txts:
        line_number, matcher = strategy( path, txt )
        if ( line_number < 1 ):
            # heuristics didn't work, go by line length estimation
            line_number = line_lenght_histo( path, txt )
        txt_starts[ txt ] = ( line_number, matcher )
    return txt_starts

def find_story_end( path ):
    txts = utils.get_file_names_by_extension( path, "txt" )
    txt_ends = {}
    for txt in txts:
        txt_ends[ txt ] = match_story_end_clues( path, txt )
    return txt_ends

def mark_story_lines( line_ranges, path ):
    for title, line_range in line_ranges.items():
        cropped_file = open( os.path.join( utils.TXTS_AS_DATA, os.path.basename( path ), title ), "w" )
        with open( os.path.join( path, title ), "r" ) as txt:
            line = txt.readline()
            idx = 1
            while line:
                if idx in line_range:
                    cropped_file.write( "[+]" + line )
                else:
                    cropped_file.write( "[-]" + line )
                line = txt.readline()
                idx += 1
        cropped_file.close()

def test_find_story_start():
    for file_name in utils.get_file_names_by_extension( "Problematic", "txt"):
        if "POP" in file_name:
            os.remove( os.path.join( "Problematic", file_name ) )
    ground_truth = {}
    with open( 'gold.csv' ) as csv_file:
        spamreader = csv.reader( csv_file, delimiter=",", quotechar="\"" )
        for row in spamreader:
            ground_truth[ row[0] ] = row[1]
    correct = 0
    # match_story_start_clues
    # match_towards_top
    strategy = collect_and_analyse_clues
    found = find_story_start( utils.BEST_SELLING_FULLTEXT, strategy )
    found.update( find_story_start( utils.POPULAR_FULLTEXT, strategy ) )
    for title in ground_truth:
        found_line_number = found[ title ][0]
        ground_truth_line_number = int( ground_truth[ title ] )
        leniency = 5
        if ( ground_truth_line_number - leniency ) <= found_line_number <= ( ground_truth_line_number + leniency ):
            correct += 1
            # print( "accurate", end="" )
            # print(  " (found: {}, gold: {})".format( found_line_number, ground_truth_line_number ), title, found[ title ][1] )
        else:
            print( "INCORRECT", end="" )
            print(  " (found: {}, gold: {})".format( found_line_number, ground_truth_line_number ), title, found[ title ][1] )
            if "POP" in title:
                shutil.copyfile( os.path.join( utils.POPULAR_FULLTEXT, title ), os.path.join( "Problematic", title ) )
    accuracy = correct/len(ground_truth) * 100
    print( "Accuracy:", accuracy )

def shape_data( path, strategy ):
    txt_starts = find_story_start( path, strategy )
    txt_ends = find_story_end( path )
    line_ranges = {}
    for txt in txt_starts.keys():
        line_ranges[ txt ] = range( txt_starts[txt][0], txt_ends[txt][0] )
    mark_story_lines( line_ranges, path )

def post_process( path ):
    print( "Post processing: {}".format( os.path.join( utils.TXTS_AS_DATA, path ) ) )
    txts = utils.get_file_names_by_extension( os.path.join( utils.TXTS_AS_DATA, path ), "txt" )
    for txt in txts:
        text = ""
        with open( os.path.join( utils.TXTS_AS_DATA, path, txt ), "r" ) as text_file:
            line = text_file.readline()
            while line:
                # illustration markers
                line = re.sub( r"^\[\+\](\.*?\[.*?illustration.*?\].*?)$", r"[-]\1", line, flags=re.IGNORECASE )
                # probably chapter/part/page/note numbers
                line = re.sub( r"^\[\+\](\s*\[ \d+ \]\s*)$", r"[-]\1", line, flags=re.IGNORECASE )
                line = re.sub( r"^\[\+\](\s*\[ \d+ \]\s*)$", r"[-]\1", line, flags=re.IGNORECASE )
                line = re.sub( r"^(\[\+\].*?)({\s*\d+\s*})(.*)?", r"\1[->\2<-]\3", line, flags=re.IGNORECASE )
                line = re.sub( r"^(\[\+\].*?)(\[\s*\d+\s*\])(.*)?", r"\1[->\2<-]\3", line, flags=re.IGNORECASE )
                line = re.sub( r"^\[\+\](\s*chapter\s*[\dixvlotfsen]+)", r"[-]\1", line, flags=re.IGNORECASE )
                text += line
                line = text_file.readline()
        with open( os.path.join( utils.TXTS_AS_DATA, path, txt ), "w" ) as text_file:
            text_file.write( text )

## MAIN
if __name__ == "__main__":
    print( utils.TXTS_AS_DATA )
    strategy = collect_and_analyse_clues
    shape_data( utils.BEST_SELLING_FULLTEXT, strategy )
    shape_data( utils.POPULAR_FULLTEXT, strategy )
    post_process( utils.BEST_SELLING_FULLTEXT )
    post_process( utils.POPULAR_FULLTEXT )
