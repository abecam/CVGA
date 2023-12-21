---
title: "Samples"
description: "See what's possible with Blowfish."

cascade:
  showEdit: false
  showSummary: false
  hideFeatureImage: false
---

{{< lead >}}
Blowfish brings your content to life. :heart_eyes:
{{< /lead >}}

This section contains some demo pages that show how Blowfish renders different types of content. You can also see an example [taxonomy listing]({{< ref "tags" >}}) page.

## YouTube

Below is an example using the built-in `youtube` shortcode.

{{< youtube ZJthWmvUzzc >}}

## Twitter

This example uses the `twitter_simple` shortcode to output a Tweet. It requires two named parameters `user` and `id`.

{{< twitter_simple user="DesignReviewed" id="1085870671291310081" >}}

Alternatively, the `tweet` shortcode can be used to embed a fully marked up Twitter card.

## Vimeo

The `vimeo_simple` shortcode will embed a Vimeo video.

{{< vimeo_simple 48912912 >}}

{{< carousel images="gallery/*" interval="2500" >}}

![Alt text](image.jpg "Image caption")

{{< gallery >}}
  <img src="gallery/01.jpg" class="grid-w50 md:grid-w33 xl:grid-w25" />
  <img src="gallery/02.jpg" class="grid-w50 md:grid-w33 xl:grid-w25" />
  <img src="gallery/03.jpg" class="grid-w50 md:grid-w33 xl:grid-w25" />
  <img src="gallery/04.jpg" class="grid-w50 md:grid-w33 xl:grid-w25" />
  <img src="gallery/05.jpg" class="grid-w50 md:grid-w33 xl:grid-w25" />
  <img src="gallery/06.jpg" class="grid-w50 md:grid-w33 xl:grid-w25" />
  <img src="gallery/07.jpg" class="grid-w50 md:grid-w33 xl:grid-w25" />
{{< /gallery >}}

{{< list limit=2 >}}

_**Sidenote:** This page is just a standard Blowfish article listing and Hugo has been configured to generate a `samples` content type and display article summaries._

---
