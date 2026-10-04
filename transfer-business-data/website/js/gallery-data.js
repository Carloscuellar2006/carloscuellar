/*
  Before & After gallery data.

  type: "slider"  -> interactive drag-to-reveal comparison
  type: "static"  -> plain side-by-side before/after, no drag

  Images are hosted on GHL's media library (uploaded via Media Storage).
*/
const CDN = "https://assets.cdn.filesafe.space/v8QzAzr7K3RAa3YQ2t0A/media/";

const galleryData = [
  {
    id: "slider-1",
    type: "slider",
    label: "Patio Cleaning — Huntsville, AL",
    before: CDN + "6a76d72b8880872019852616.jpg",
    after: CDN + "6a76d72b9a9c7792eaa9c964.jpg"
  },
  {
    id: "slider-2",
    type: "slider",
    label: "Concrete Alcove Cleaning — Huntsville, AL",
    before: CDN + "6a76d72403343f290fd37bc4.jpg",
    after: CDN + "6a76d7248880872019850576.jpg"
  },
  {
    id: "slider-3",
    type: "slider",
    label: "Paver Patio & Fire Pit Cleaning — Huntsville, AL",
    before: CDN + "6a76d72a9994d35aa025f59c.jpg",
    after: CDN + "6a76d7275a64f2b5677ba82f.jpg"
  },
  {
    id: "static-1",
    type: "static",
    label: "Brick Wall Cleaning — Huntsville, AL",
    before: CDN + "6a76d7285a64f2b5677ba839.jpg",
    after: CDN + "6a76d7275a64f2b5677ba825.jpg"
  },
  {
    id: "static-2",
    type: "static",
    label: "Paver Patio Cleaning — Huntsville, AL",
    before: CDN + "6a76d7279a9c7792eaa9c934.jpg",
    after: CDN + "6a76d7285a64f2b5677ba83e.jpg"
  },
  {
    id: "static-3",
    type: "static",
    label: "Landscape Bed Cleanup — Huntsville, AL",
    before: CDN + "6a76d72a8880872019851fa7.jpg",
    after: CDN + "6a76d72b9a9c7792eaa9c95e.jpg"
  },
  {
    id: "static-4",
    type: "static",
    label: "Retaining Wall Cleaning — Huntsville, AL",
    before: CDN + "6a76d7299a9c7792eaa9c94c.jpg",
    after: CDN + "6a76d7289a9c7792eaa9c93e.jpg"
  },
  {
    id: "static-5",
    type: "static",
    label: "Driveway Cleaning — Huntsville, AL",
    before: CDN + "6a76d7249994d35aa025e3d2.jpg",
    after: CDN + "6a76d72b5a64f2b5677ba873.jpg"
  },
  {
    id: "static-6",
    type: "static",
    label: "Sidewalk Cleaning — Huntsville, AL",
    before: CDN + "6a76d72c03343f290fd38fdd.jpg",
    after: CDN + "6a76d72403343f290fd37bbf.jpg"
  },
  {
    id: "static-7",
    type: "static",
    label: "Sidewalk Cleaning — Huntsville, AL",
    before: CDN + "6a76d7245a64f2b5677ba80f.jpg",
    after: CDN + "6a76d7248880872019850555.jpg"
  }
];
