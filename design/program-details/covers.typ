// Front + back cover art alone, full-bleed — for Lulu's cover creator.
// Build with:  typst compile --font-path fonts --input target=covers covers.typ
#import "template.typ": *
#show: conf
#cover()
#backcover()
