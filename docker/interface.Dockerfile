FROM node

ADD /interface /interface

WORKDIR /interface

RUN npm install

ENTRYPOINT ["npm", "run"]
CMD ["dev", "--", "--host", "0.0.0.0"]
