# blue_canvas_interview (XML project)

Algorithm
=====
First the XML is converted into a hashable data type (dictionaries) that allows O(1) lookup when comparing, so our comparison algorithm becomes O(n). The bulk of the time is spent on this step, since it requires loading both the left and right datasets then a O(n) algorithm to convert each of them. The algorithm to convert is a just a recursive depth_first function that follows the XML tree and creates a hashmap of keys to lists. Nodes without children are represented by lists of strings, with identical tags being grouped together ("scopes" in the example set) for easy comparison.

Once the dictionaries are produced, comparison starts in O(2n) time, visiting each element of the left and comparing it to the right element, then doing the reverse to check if keys exist in the right but not the left. If the algorithm encounters another dictionary (a layer of depth in the XML), it calls itself recursively. It keeps a stack of ancestors to identify where there are differences.

Cases that break the algorithm
-----
Since this was a quick project, some concessions had to be made. If two identically-named tags have children, the algorithm will break if they are not in the same order on both left and right. This could be solved by an additional algorithm that "scored" the similarity of the children and matched them but would greatly increase the complexity of the project. The algorithm also does not check tag attributes currently.

Benchmarking
-----
Since the only (large) pieces of data is the XML itself, and that data can be safely discarded once converted to a dictionary, the heap memory this program takes up is O(3n), assuming the data sets are the same size and the garbage collector kills the XML on conversion. So we could likely compare two 42 MB datasets.

A ~23mb open source set from NASA was used for benchmarking, compared against itself. The 46 mb total dataset took ~2.5 seconds. The loading and converting took ~2 seconds and the comparison took .5 seconds. Since we expect the loading to be O(4n) (loading from file twice and converting to dictionaries twice) and the comparison to be O(n), this is exactly in line with what we expect. In 100ms we could compare about 2 MB sum of both sets. 

Further steps
=====
With two weeks' time, the first thing I would do is see if I could create a hashable data type in-place in lxml trees. There might be a way to do this currently but my research didn't turn up much. This would change the algorithm from O(5n) to O(3n). and improve max memory usage to 2n. The second thing I would do is fix the afforementioned edge cases, starting with checking attributes then moving onto the other issue.

I would also import the xmltodict library that someone developed, if needed. I avoided it for this project since it seemed to be against the spirit of the project.

I would probably put some kind of git-like front-end for comparing changes instead of using the terminal.

Lastly I'd improve the parsing. I didn't do much work to make sure encoding worked appropriately and just worked in UTF-8, and I'm sure there's some edge cases with poorly formatted XML that would break the code.