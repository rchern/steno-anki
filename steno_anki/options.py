from optparse import OptionParser

opts = OptionParser()
opts.add_option('-i', '--input', dest='input', default='decks')
opts.add_option('-o', '--output', dest='output', default='plover.apkg')
opts.add_option('-d', '--diagrams', dest='diagrams', default='diagrams')

values, args = opts.parse_args()

print(values)