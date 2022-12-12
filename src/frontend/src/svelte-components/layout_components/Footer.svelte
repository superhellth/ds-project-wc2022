<script>
  // Adds a footer to the webpage
    import {Container} from "sveltestrap";

    export let color = "";
    let bg_color = "bg-" + color;
</script>


<footer class="py-4 {bg_color} mt-auto">
  <Container fluid={true}>
    <div class="d-flex align-items-center justify-content-between small">
      <div class="text-muted ">
        Made by
        <a href="mailto:nicolas.hellthaler@stud.uni-heidelberg.de">Nico Hellthaler</a>,
        <a href="mailto:ve257@stud.uni-heidelberg.de">Raphael Ebner</a> and
        <a href="mailto:bastian.mueller@stud.uni-heidelberg.de">Bastian Müller</a>.
        Made possible by <a href="https://www.twitter.com">Twitter</a>, a bunch of Text Analytics tools and favorite tool <a href="https://openai.com/blog/chatgpt/">chatGPT by OpenAI</a>.
      </div>
    </div>
  </Container>
</footer>
