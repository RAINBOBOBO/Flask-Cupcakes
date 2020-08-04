"use strict"

async function getCupcakes(){
  console.log("getCupcakes")
  let response = await axios.get("/api/cupcakes");
  const cupcakesInDB = response.data.cupcakes;
  // console.log("this is cupcakesInDB", cupcakesInDB)

  return cupcakesInDB;
}

async function putCupcakesOnPage(){
  console.log("putCupcakesOnPage")
  let cupcakes = await getCupcakes()
  let $list = $('#cupcake-list');

  for (let cupcake of cupcakes){
    const $cupcakeHolder = $(
      `<li>
      <img src='${cupcake.image}'>
      flavor: ${cupcake.flavor}, size: ${cupcake.size}, rating: ${cupcake.rating}
      </li>`
    )
    $list.append($cupcakeHolder);
  }
}

async function submitForm(evt){
  console.log("submit form")
  evt.preventDefault();

  let flavor = $("#cupcake-flavor").val();
  let image = $("#cupcake-image").val();
  let size = $("#cupcake-size").val();
  let rating = $("#cupcake-rating").val();

  // console.log("This is response:", response)
  const response = await axios.post('http://localhost:5000/api/cupcakes', 
    {
      "flavor": flavor,
      "image": image,
      "size": size,
      "rating": rating
    });
}
$("#add-cupcake").on("submit", submitForm)

putCupcakesOnPage()

// This one is more consistant to code
// await axios({
//   url: 'http://localhost:5000/api/cupcakes',
//   method: "POST",
//   data: {
//     "flavor": flavor,
//     "image": image,
//     "size": size,
//     "rating": rating
//   }
// });