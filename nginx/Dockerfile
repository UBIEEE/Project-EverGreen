FROM nginx

COPY . .

# Copy SSL cert files, if they exist
RUN if [ -f ./cert.pem ]; then cp ./cert.pem /etc/nginx/cert.pem; fi
RUN if [ -f ./private.key ]; then cp ./private.key /etc/nginx/private.key; fi

# Choose whether to use SSL (default) or HTTP-only conf based on above existing
RUN if [ -f ./cert.pem -a -f ./private.key ]; \
        then cp ./default.conf /etc/nginx/conf.d/default.conf; \
        else cp ./no_ssl.conf /etc/nginx/conf.d/default.conf; fi;
