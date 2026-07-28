# G11 – Senior Developer (Integration)

CONTROLLED July - 26

## Important Constraint

Do not query GeoServer or the Derbyshire web service directly from client-side JavaScript because of CORS restrictions.

Your solution should use an appropriate server-side, backend, or alternative approach.

## Requirements

Your solution should:

- Use the Address Lookup API to search for DE55 5PB.
- Identify the address record corresponding to HILLBROW.
- Use that record’s coordinates to query GeoServer.
- Find the nearest grit bin within approximately 100 metres.
- Return the grit bin Title.
- Handle cases where the address is not found.
- Handle cases where no grit bin is found nearby.
- Include clear error handling and assumptions.

## What We Are Looking For

Although there is a correct result, we are also interested in how you approach the problem.

We are looking for evidence that you can:

- Break the problem down into manageable parts.
- Research unfamiliar APIs or services.
- Identify the correct GeoServer service to use.
- Work with different response schemas.
- Appreciate API capabilities such as coordinate systems and spatial queries.
- Work around CORS restrictions appropriately.
- Explain your reasoning.
- Produce readable and maintainable code.

## Investigation Notes

As part of your response, please include brief notes explaining how you investigated the problem.

For example:

- What did you try first?
- What tools you used?
- What documentation or resources did you use?
- What assumptions did you make?
- Were there any approaches you rejected?
- How did you verify the result?

## Deliverables

Please demonstrate:

- The solution running.
- The grit bin Title returned by your solution.
- A short explanation covering:
  - your approach
  - assumptions made
  - any issues encountered
  - how you investigated those issues
  - what you would improve with more time
  - how it could be deployed or reused

## Follow-up Discussion

Be prepared to discuss:

- How you would make the solution reusable for other asset types.
- How you would adapt it to return the nearest five grit bins.
- How you would make functionality available to other Solutions.
- How you would process a large batch of addresses.
- How you would test and monitor the solution if it became a production service.
