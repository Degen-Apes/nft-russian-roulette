FROM node as CTR_BUILDER

ADD /contracts /contracts

WORKDIR /contracts

RUN npm install
RUN npx hardhat compile


FROM python:3.9 as RUNNER

ADD /backend /backend

WORKDIR /backend

RUN pip install -U poetry
RUN make install-dev

RUN which poetry

ADD /contracts /contracts
COPY --from=CTR_BUILDER /contracts/artifacts /contracts/artifacts

ENTRYPOINT ["/usr/local/bin/poetry", "run"]
