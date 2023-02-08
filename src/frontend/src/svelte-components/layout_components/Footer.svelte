<script>
    // Import the Container component from the svelte-strap library
    import {Container} from "sveltestrap";

    // Define a variable for the background color of the footer
    export let color = "";

    // Create a variable for the class name for the background color
    let bg_color = "bg-" + color;
</script>


<footer class="py-4 mt-auto" style="background-color: var(--nav-bar-color)">
  <Container fluid={true}>
    <div class="d-flex align-items-center justify-content-between small">
      <div class="text-muted ">
        Made by
        <a href="mailto:nicolas.hellthaler@stud.uni-heidelberg.de">Nico Hellthaler</a>,
        <a href="mailto:ve257@stud.uni-heidelberg.de">Raphael Ebner</a> and
        <a href="mailto:bastian.mueller@stud.uni-heidelberg.de">Bastian Müller</a>.
        Made possible by <a href="https://www.twitter.com">Twitter</a>, a bunch of Text Analytics tools and our good friend <a href="https://openai.com/blog/chatgpt/">chatGPT</a> by OpenAI.
      </div>
    </div>
  </Container>
</footer>

<style lang="scss">
  // a {
  //   color: var(--twitter-dimmed-primary-color);
  // }
</style>