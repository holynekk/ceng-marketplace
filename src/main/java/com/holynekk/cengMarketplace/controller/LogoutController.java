package com.holynekk.cengMarketplace.controller;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.client.registration.ClientRegistrationRepository;
import org.springframework.security.web.authentication.logout.SecurityContextLogoutHandler;
import org.springframework.stereotype.Controller;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;
import org.springframework.web.util.UriComponentsBuilder;

@Controller
public class LogoutController extends SecurityContextLogoutHandler {

  @Autowired private ClientRegistrationRepository registrationRepository;

  @Override
  public void logout(
      HttpServletRequest request, HttpServletResponse response, Authentication authentication) {
    super.logout(request, response, authentication);
    String issuer =
        (String)
            registrationRepository
                .findByRegistrationId("auth0")
                .getProviderDetails()
                .getConfigurationMetadata()
                .get("issuer");
    String clientId = registrationRepository.findByRegistrationId("auth0").getClientId();

    String returnTo = ServletUriComponentsBuilder.fromCurrentContextPath().build().toString();

    String logoutURL =
        UriComponentsBuilder.fromHttpUrl(
                issuer + "/v2/logout?client_id={clientId}&returnTo={returnTo}")
            .encode()
            .buildAndExpand(clientId, returnTo)
            .toUriString();

    try {
      response.sendRedirect(logoutURL);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
