# pandoc-cover

Add a cover to a pdf document using an SVG template and the pandoc metadata.

## Example

1. Create a SVG template called `foo.svg`. Write
   `{{ title }}` in place of the title and `{{ whatever }}`
   in place of whatever information you want to display on
   the cover (see `templates/sample_front.j2.svg` for an example).

2. Add `title` and `whatever` variables in your `bar.md` document

   ```yaml
   title: 'Hello World !'
   whatever: 'This is so simple'
   pandoc-cover:
     front: 'path/to/foo.svg'
   ```

3. Launch pandoc with the pandoc_cover filter.

    ```
    pandoc --filter=pandoc-cover bar.md -o bar.pdf
    ```

