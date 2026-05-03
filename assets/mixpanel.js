/**
 * Mixpanel browser wrapper for namealigned.com (static HTML).
 *
 * Loads the official Mixpanel browser SDK from CDN, initialises with the
 * public project token, and exposes three globals used across the site:
 *   - window.naTrack(name, props)        // event tracking
 *   - window.naIdentify(email, props)    // identify + people set
 *   - window.naReset()                   // logout / clear identity
 *
 * The existing trackEvent() helper in analyzer.html will also call naTrack
 * when present, so legacy events keep working with no changes.
 *
 * To set the token: replace the placeholder below with your project token
 * from Mixpanel → Project Settings. This is a PUBLIC token and is safe in
 * client code.
 */
(function(){
  // ── 1. PUBLIC TOKEN ────────────────────────────────────────────────
  // Replace with your Mixpanel project token.
  var MIXPANEL_TOKEN = 'YOUR_MIXPANEL_TOKEN';

  // No-op everything if the token hasn't been set yet (avoids junk events
  // hitting whatever default project the placeholder maps to).
  if (!MIXPANEL_TOKEN || MIXPANEL_TOKEN === 'YOUR_MIXPANEL_TOKEN') {
    window.naTrack    = function(){ /* mixpanel token not set */ };
    window.naIdentify = function(){};
    window.naReset    = function(){};
    return;
  }

  // ── 2. Load Mixpanel browser SDK (official snippet, minified) ──────
  (function(f,b){if(!b.__SV){var e,g,i,h;window.mixpanel=b;b._i=[];b.init=function(e,f,c){function g(a,d){var b=d.split(".");2==b.length&&(a=a[b[0]],d=b[1]);a[d]=function(){a.push([d].concat(Array.prototype.slice.call(arguments,0)))}}var a=b;"undefined"!==typeof c?a=b[c]=[]:c="mixpanel";a.people=a.people||[];a.toString=function(a){var d="mixpanel";"mixpanel"!==c&&(d+="."+c);a||(d+=" (stub)");return d};a.people.toString=function(){return a.toString(1)+".people (stub)"};i="disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking start_batch_senders people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");
  for(h=0;h<i.length;h++)g(a,i[h]);var j="set set_once union unset remove delete".split(" ");a.get_group=function(){function b(c){d[c]=function(){call2_args=arguments;call2=[c].concat(Array.prototype.slice.call(call2_args,0));a.push([e,call2])}}for(var d={},e=["get_group"].concat(Array.prototype.slice.call(arguments,0)),c=0;c<j.length;c++)b(j[c]);return d};b._i.push([e,f,c])};b.__SV=1.2;e=f.createElement("script");e.type="text/javascript";e.async=!0;e.src="undefined"!==typeof MIXPANEL_CUSTOM_LIB_URL?MIXPANEL_CUSTOM_LIB_URL:"file:"===f.location.protocol&&"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\/\//)?"https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js":"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";g=f.getElementsByTagName("script")[0];g.parentNode.insertBefore(e,g)}})(document,window.mixpanel||[]);

  // ── 3. Init ────────────────────────────────────────────────────────
  window.mixpanel.init(MIXPANEL_TOKEN, {
    debug: false,
    track_pageview: true,
    persistence: 'localStorage',
    ignore_dnt: false,
  });

  // ── 4. Public wrappers ────────────────────────────────────────────
  window.naTrack = function(name, props){
    try { window.mixpanel.track(name, props || {}); }
    catch(e){ console.warn('[mixpanel] track failed', name, e); }
  };

  window.naIdentify = function(email, props){
    try {
      if (!email) return;
      window.mixpanel.identify(email);
      window.mixpanel.people.set(Object.assign({ $email: email }, props || {}));
    } catch(e){ console.warn('[mixpanel] identify failed', e); }
  };

  window.naReset = function(){
    try { window.mixpanel.reset(); } catch(e){}
  };
})();
