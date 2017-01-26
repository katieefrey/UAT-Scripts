The folder "scripts for skos xl" contains the same scripts as this folder, but they work for UAT verion 1.01 and below, when the UAT was being produced in skos-xl format.  The current version of the UAT is in the skos format.

This folder contains scripts that manipulate the RDF file exported from VocBench into other useful and/or interesting formats.

Only run UAT_SKOS_master.py, it will call the other scripts.  However, you can comment out any of the others scripts from the bottom of the master script.

Resulting files:

1) A series of html files used to support both the hierarchical and alphabetical browers of the UAT
 #execfile("UAT_SKOS_to_html.py")

2) A CSV flatfile that displays the hierarchy of the thesaurus
 #execfile("UAT_SKOS_to_flatfile.py")

3) A CSV file detailing all 'related to' links in the UAT
 #execfile("UAT_SKOS_to_related_list.py")

4) A json file with the structure of the UAT, used for the visual browser
 #execfile("UAT_SKOS_to_dendrogram.py")

5) Another json file with the UAT structure that also includes the sum of each terms child terms
 #execfile("UAT_SKOS_to_dendrogram-with-child-nums.py")

6) A json file for use with the UAT API that lists all concepts
 #execfile("UAT_SKOS_to_json_flat_for_allconcepts_api.py")

7) Three csv files, one of which is just a striaght list of all concepts in the UAT, the second is a straight list of all concepts with all alternative terms, and the third is a list of all concepts with their URIs.
 #execfile("UAT_SKOS_to_csv_lists.py")

8) A javascript file for use in the UAT autocomplete widget
 #execfile("UAT_SKOS_to_autocomplete.py")
