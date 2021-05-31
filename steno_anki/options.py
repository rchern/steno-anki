from optparse import OptionParser

opts = OptionParser()
opts.add_option('-i', '--input', dest='input', default='decks')
opts.add_option('-o', '--output', dest='output', default='plover.apkg')

values, args = opts.parse_args()

print(values)