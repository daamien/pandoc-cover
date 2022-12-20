# pandoc-cover

Add a PDF cover to document using an SVG template and
the document metadata.

Currently, this only works if you are also using the
`eisvogel` template


## Example

1. Create a SVG template called `foo.svg` and write
   `{{ metadata.title }}` in place of the title.

2. Add a `title` metadata in your pandoc document

3. Activate the plugin in the header of your document (`bar.md`)

   ```yaml
   title: 'Hello World !"
   titlepage: false
   titlepage-background: 'path/to/foo.svg'
   ```

4. Launch pandoc

    ```
    pandoc --filter=pandoc_cover --template=eisvogel bar.md -o bar.pdf
    ```
