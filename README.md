# pandoc-cover

Add a PDF cover to document using an SVG template and
the document metadata.

Currently, this only works if you are also using the
`eisvogel` template


## Example

1. Create a SVG template called `foo.svg`. Write
   `{{ title }}` in place of the title and `{{ whatever }}`
   in place of whatever information you want to appear on
   the cover.

2. Add `title` and `whatever` variables in your pandoc document
   (`bar.md`)

3. Disable the eivogel titlepage and define your SVG template as
   the titlepage background (`bar.md`).

4. The `bar.md` header should look like this:

   ```yaml
   title: 'Hello World !"
   whatever: 'this is so simple'
   titlepage: false
   titlepage-background: 'path/to/foo.svg'
   ```

5. Launch pandoc with eisvgel and the pandoc_cover filter.

    ```
    pandoc --filter=pandoc_cover --template=eisvogel bar.md -o bar.pdf
    ```
